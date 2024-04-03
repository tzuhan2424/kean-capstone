import pandas as pd
import numpy as np
import urllib3
import datetime
import MySQLdb
import time
import sys
import pydap.client as pydapclient
from settings import DATABASES


class ETLLogger:
    def __init__(self, log_file_dir: str=None):
        self._depth = -1
        self._file = None

        if log_file_dir is not None:
            # Append time to log file name to make it unique
            self._file = open(f'{log_file_dir}/etl_log_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt', 'w')

    def __del__(self):
        if self._file is not None:
            self._file.close()

    def get_log_token(self, message: str):
        ''' Prints a logging start message and returns a log token. When the token object is
        deleted, such as by going out of scope, the end message is shown along with the time
        elapsed. Each token increases the depth of the log hierarchy.
        '''
        return _LogToken(self, message)

    def _log_start(self, message: str):
        text = '  ' * self._depth + f'[START] {message}'
        print(text)

        if self._file is not None:
            self._file.write(text + '\n')

    def _log_end(self, message: str):
        text = '  ' * self._depth + f'[END]   {message}'
        print(text)

        if self._file is not None:
            self._file.write(text + '\n')


class _LogToken:
    def __init__(self, logger: ETLLogger, message: str):
        self._logger = logger
        self._message = message
        self._start_time = time.time()
        self._logger._depth += 1
        self._logger._log_start(message)

    def __del__(self):
        self._logger._log_end(f'{self._message} (time elapsed: {time.time() - self._start_time:.3f} s)')
        self._logger._depth -= 1


class HABDataETLHelper:
    _api_columns = ['STATE_ID', 'DESCRIPTION', 'LATITUDE', 'LONGITUDE', 'SAMPLE_DATE', 'SAMPLE_DEPTH',
                'GENUS', 'SPECIES', 'CATEGORY', 'CELLCOUNT', 'CELLCOUNT_UNIT', 'CELLCOUNT_QA',
                'SALINITY', 'SALINITY_UNIT', 'SALINITY_QA', 'WATER_TEMP', 'WATER_TEMP_UNIT', 'WATER_TEMP_QA',
                'WIND_DIR', 'WIND_DIR_UNIT', 'WIND_DIR_QA', 'WIND_SPEED', 'WIND_SPEED_UNIT', 'WIND_SPEED_QA']
    _api_datatypes = [pd.StringDtype(), pd.StringDtype(), np.float64, np.float64, None, np.float64,
                  pd.StringDtype(), pd.StringDtype(), pd.StringDtype(), np.float64, pd.StringDtype(), np.int64,
                  np.float64, pd.StringDtype(), np.int64, np.float64, pd.StringDtype(), np.int64,
                  np.float64, pd.StringDtype(), np.int64, np.float64, pd.StringDtype(), np.int64]
    _required_columns = ['LATITUDE', 'LONGITUDE', 'SAMPLE_DATE', 'CELLCOUNT']

    def __init__(self, database_table_name: str, logger: ETLLogger=None) -> None:
        self._df = None
        self._logger = logger
        self._database_table_name = database_table_name

    def get_dataframe(self) -> pd.DataFrame:
        ''' Returns data as dataframe.'''
        return self._df

    def run_etl_from_api(self, start_date: datetime.datetime, end_date: datetime.datetime, start_date_exclusive: bool=False,
                         supplement_from_weather_data: bool=True, date_delta: datetime.timedelta=datetime.timedelta(days=1.0),
                         latlong_delta: float=0.1, allow_nan_rows: bool=False) -> None:
        ''' Run extraction, transformation, and loading using the NOAA
        API as the data source and the TideTrack database as the data
        sink.

        Parameters:
        start_date: Start sample date for extraction, inclusive. If
        None, then the latest time in the database is used, exclusive.
        Default is None.
        end_date: End sample date for extraction, inclusive. If None,
        then the current time is used. Default is None.
        supplement_from_weather_data: Whether to supplement missing
        data from different weather datasets. Default is True.
        date_delta: Maximum difference between HAB and weather data
        sample dates for merging. Default is 1 day.
        latlong_delta: Maximum difference between HAB and weather
        data latitude and longitude for merging. Default is 0.1.
        allow_nan_rows: Whether to allow rows with missing values to be
        loaded into the MySQL database. Default is False.'''
        self.transform_from_api(
            self.extract_from_api(start_date=start_date,
                                  end_date=end_date,
                                  start_date_exclusive=start_date_exclusive))

        # If requested, supplement missing rows from weather dataset
        if supplement_from_weather_data:
            self.merge_with_weather_data_from_api(start_date=start_date,
                                                  end_date=end_date,
                                                  date_delta=date_delta,
                                                  latlong_delta=latlong_delta)

        self.load_to_database(allow_nan_rows=allow_nan_rows)

    def extract_from_api(self, start_date: datetime.datetime, end_date: datetime.datetime, start_date_exclusive: bool) -> dict:
        ''' Extracts HAB data from NOAA API. Returns extracted JSON
        data.

        Parameters:
        start_date: Start sample date for extraction.
        end_date: End sample date for extraction, inclusive.
        start_date_exclusive: Whether start date is inclusive (False)
        or exclusive (True).'''
        log = self._GetLogger('Extracting HAB data from API')

        # Form "where" field. Must use spaces between all operators, even "=", else API query fails.
        where = 'GENUS = \'Karenia\' AND SPECIES = \'brevis\''

        if start_date != None:
            where += f' AND SAMPLE_DATE >{"" if start_date_exclusive else "="} timestamp \'{start_date.strftime("%Y-%m-%d %H:%M:%S")}\''

        if end_date != None:
            where += f' AND SAMPLE_DATE <= timestamp \'{end_date.strftime("%Y-%m-%d %H:%M:%S")}\''

        # Request from NOAA API
        response = urllib3.request(method='GET',
                                   url='https://gis.ncdc.noaa.gov/arcgis/rest/services/ms/HABSOS_CellCounts/MapServer/0/query',
                                   timeout=300.0,  # Allow 5 minutes due to large data volume
                                   fields={ 'f': 'json',
                                            'where': where,
                                            'outFields': ','.join(HABDataETLHelper._api_columns),
                                            'returnGeometry': 'false' })

        if response.status == 200:
            # Convert to JSON. Throws expection for invalid JSON.
            return response.json()
        else:
            raise Exception(f'HTTP request failed. Status: {response.status}')

    def transform_from_api(self, json_data: dict) -> None:
        '''Transforms JSON data extracted from NOAA API.'''
        log = self._GetLogger('Transforming HAB data from API')

        # JSON dictionary accesses will throw an exception if JSON keys are not as expected. This is OK.
        transformed_data = {}

        # Parse fields to column arrays
        for field in json_data['fields']:
            transformed_data[field['name']] = []

        # Extract data into format for dataframe
        for feature in json_data['features']:
            for field in transformed_data.keys():
                transformed_data[field].append(feature['attributes'][field])

        # Special case: Convert UNIX millisecond timestamp to datetime.
        for row_index in range(len(transformed_data['SAMPLE_DATE'])):
            transformed_data['SAMPLE_DATE'][row_index] = datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds=int(transformed_data['SAMPLE_DATE'][row_index] / 1000))

        transformed_data = pd.DataFrame(transformed_data)

        # Convert column data types
        for column_index in range(len(HABDataETLHelper._api_columns)):
            if HABDataETLHelper._api_datatypes[column_index] is not None:
                # Skip None data types (i.e., do not convert)
                transformed_data[HABDataETLHelper._api_columns[column_index]] = transformed_data[HABDataETLHelper._api_columns[column_index]].astype(HABDataETLHelper._api_datatypes[column_index])

        # Assign dataframe if successful (i.e., no exceptions thrown)
        self._df = transformed_data

    def load_to_database(self, allow_nan_rows: bool) -> None:
        '''Loads dataframe to MySQL database.

        Parameters:
        allow_nan_rows: Whether to allow rows with missing values to be
        loaded into the MySQL database.'''
        log = self._GetLogger('Loading HAB data to database')

        # Database uses VARCHAR for SAMPLE_DATE column and DATETIME for
        # SAMPLE_DATETIME column to represent the same date
        extra_columns = ['SAMPLE_DATETIME']

        # Connect to database
        db = MySQLdb.connect(host=DATABASES['default']['HOST'],
                             port=int(DATABASES['default']['PORT']),
                             database=DATABASES['default']['NAME'],
                             user=DATABASES['default']['USER'],
                             password=DATABASES['default']['PASSWORD'])
        db_cursor = db.cursor()

        # Table does not allow null values on some columns. If
        # requested, do not allow rows with missing values in any
        # column.
        if allow_nan_rows:
            df_no_nan = self._df.dropna(subset=HABDataETLHelper._required_columns)
        else:
            df_no_nan = self._df.dropna()

        # Optimize insert by using a parametrized query and call executemany
        query = f'INSERT INTO {self._database_table_name}({",".join(HABDataETLHelper._api_columns + extra_columns)}) VALUES ({",".join(["%s"] * (len(HABDataETLHelper._api_columns) + len(extra_columns)))})'

        # Insert rows
        query_values = []
        for row_index in df_no_nan.index:
            row_values = []

            for column_index in range(len(HABDataETLHelper._api_columns)):
                if HABDataETLHelper._api_columns[column_index] == 'SAMPLE_DATE':
                    # Maintain this date format, as required by front end
                    row_values.append(f'{df_no_nan[HABDataETLHelper._api_columns[column_index]][row_index].strftime("%m/%d/%Y %H:%M")}')
                elif pd.isnull(df_no_nan[HABDataETLHelper._api_columns[column_index]][row_index]):
                    row_values.append(None)
                elif HABDataETLHelper._api_datatypes[column_index] == pd.StringDtype():
                    row_values.append(f'{df_no_nan[HABDataETLHelper._api_columns[column_index]][row_index]}')
                else:
                    row_values.append(str(df_no_nan[HABDataETLHelper._api_columns[column_index]][row_index]))

            for column_index in range(len(extra_columns)):
                if extra_columns[column_index] == 'SAMPLE_DATETIME':
                    row_values.append(f'{df_no_nan["SAMPLE_DATE"][row_index].strftime("%Y-%m-%d %H:%M:%S")}')

            query_values.append(row_values)

            # # Special case: There may be bad dates in data (from conversion error or bad data). Continue execution.
            # try:
            #     db_cursor.execute(query)
            # except:
            #     pass

        db_cursor.executemany(query, query_values)

        db.commit()
        db.close()

    def extract_from_database(self) -> None:
        '''Extracts HAB data from database and stores it in internal dataframe.'''
        log = self._GetLogger('Extracting HAB data from database')

        # Connect to database
        db = MySQLdb.connect(host=DATABASES['default']['HOST'],
                             port=int(DATABASES['default']['PORT']),
                             database=DATABASES['default']['NAME'],
                             user=DATABASES['default']['USER'],
                             password=DATABASES['default']['PASSWORD'])
        db_cursor = db.cursor()

        # Request datetime sample date column from database for proper conversion
        database_columns = HABDataETLHelper._api_columns.copy()

        for column_index in range(len(database_columns)):
            if database_columns[column_index] == 'SAMPLE_DATE':
                database_columns[column_index] = 'SAMPLE_DATETIME'

        # Query for all data
        db_cursor.execute(f'SELECT {",".join(HABDataETLHelper._api_columns)} FROM {self._database_table_name}')

        data = {}
        for column in HABDataETLHelper._api_columns:
            data[column] = []

        row = db_cursor.fetchone()
        while row:
            for column_index in range(len(HABDataETLHelper._api_columns)):
                data[HABDataETLHelper._api_columns[column_index]].append(row[column_index])

            # Get next row
            row = db_cursor.fetchone()

        data = pd.DataFrame(data)

        # Convert datatypes
        for column_index in range(len(HABDataETLHelper._api_columns)):
            if HABDataETLHelper._api_datatypes[column_index] is not None:
                data[HABDataETLHelper._api_columns[column_index]].astype(HABDataETLHelper._api_datatypes[column_index])

        self._df = data

    def merge_with_weather_data_from_api(self, start_date: datetime.datetime, end_date: datetime.datetime, date_delta: datetime.timedelta, latlong_delta: float) -> None:
        ''' Merges HAB data in internal dataframe with weather data
        from NOAA API.

        Parameters:
        start_date: Start sample date for extraction, inclusive.
        end_date: End sample date for extraction, inclusive.
        date_delta: Maximum difference between HAB and weather data
        sample dates for merging.
        latlong_delta: Maximum difference between HAB and weather
        data latitude and longitude for merging.'''
        log = self._GetLogger('Merging HAB and weather data')
        weather_data = WeatherDataETLHelper(logger=self._logger)

        iteration_start_date = start_date
        iteration_end_date = end_date

        while iteration_start_date < end_date:
            # Weather data API only allows requests with a date interval within the same month, so make multiple requests
            if iteration_start_date.year != iteration_end_date.year or iteration_start_date.month != iteration_end_date.month:
                iteration_end_date = (datetime.datetime(year=iteration_start_date.year + int(iteration_start_date.month / 12),
                                                        month=iteration_start_date.month % 12 + 1,
                                                        day=1)
                                      - datetime.timedelta(days=1))

            iteration_log = self._GetLogger(f'Merging HAB and weather data from {iteration_start_date} to {iteration_end_date}')

            # Get slice of rows with any missing values within date interval
            df_slice = self._df.loc[self._df[(self._df['SAMPLE_DATE'] >= iteration_start_date) &
                                             (self._df['SAMPLE_DATE'] <= iteration_end_date)].isnull().any(axis=1).index]

            # Get columns with missing values
            columns_with_null = df_slice.keys()[df_slice.isnull().any(axis=0)].to_list()

            # Only run if there are columns with missing data (also checks if there are data in this slice)
            if len(columns_with_null) > 0:
                # Determine bounding box in (latitude, longitude) coordinates from NW to SE
                # encompassing the HAB data slice plus margin for the lat-long delta
                bounding_box = [max(df_slice['LATITUDE']) + latlong_delta,
                                min(df_slice['LONGITUDE']) - latlong_delta,
                                min(df_slice['LATITUDE']) - latlong_delta,
                                max(df_slice['LONGITUDE']) + latlong_delta]

                # Get weather data for date interval for missing columns.
                # Can sometimes fail with HTTP status 503, so try again
                # after a backoff delay.
                attempts_remaining = 3
                while attempts_remaining > 0:
                    try:
                        weather_data.run_et_from_api(start_date=iteration_start_date,
                                                    end_date=iteration_end_date,
                                                    columns=columns_with_null,
                                                    datatypes=df_slice[columns_with_null].dtypes.to_list(),
                                                    bounding_box=bounding_box)
                        attempts_remaining = 0  # Clear to exit loop
                    except:
                        attempts_remaining -= 1

                        if attempts_remaining == 0:
                            raise Exception('Weather data extract-transform operation failed.')

                        # Backoff from next request in case API server is being overwhelmed
                        time.sleep(30.0)

                weather_data_df = weather_data.get_dataframe()

                if not weather_data_df.empty:
                    merge_log = self._GetLogger('Merging HAB and weather data chunk')

                    # Replace missing HAB data with data from best match weather data row
                    # for each column. Best match is the row with the closest location.
                    for index in df_slice.index:
                        # Get weather data with date and location within deltas
                        weather_data_slice = weather_data_df[(weather_data_df['DATE'] - df_slice.loc[index, 'SAMPLE_DATE'] <= date_delta) &
                                                            (weather_data_df['DATE'] - df_slice.loc[index, 'SAMPLE_DATE'] >= date_delta) &
                                                            (abs(weather_data_df['LONGITUDE'] - df_slice.loc[index, 'LONGITUDE']) <= latlong_delta) &
                                                            (abs(weather_data_df['LATITUDE'] - df_slice.loc[index, 'LATITUDE']) <= latlong_delta)]

                        # For each column, get all rows without missing values
                        weather_data_columns_slices = {}
                        for column in columns_with_null:
                            weather_data_column_slice = weather_data_slice.dropna(subset=column)

                            # Only include columns with data
                            if len(weather_data_column_slice) > 0:
                                weather_data_columns_slices[column] = weather_data_column_slice

                        # Only try merge if any data are found for missing columns in weather data
                        if len(weather_data_columns_slices) > 0:
                            for column in weather_data_columns_slices.keys():
                                # Only attempt merge if datum is missing
                                if pd.isnull(self._df.loc[index, column]):
                                    # Get index with closest location
                                    best_match_index = np.nan
                                    best_match_distance = np.nan

                                    for weather_index in weather_data_columns_slices[column].index:
                                        long_diff = weather_data_columns_slices[column].loc[weather_index, 'LONGITUDE'] - df_slice.loc[index, 'LONGITUDE']
                                        lat_diff = weather_data_columns_slices[column].loc[weather_index, 'LATITUDE'] - df_slice.loc[index, 'LATITUDE']
                                        distance = (lat_diff ** 2 + long_diff ** 2) ** 0.5

                                        if np.isnan(best_match_index) or distance < best_match_distance:
                                            best_match_index = weather_index
                                            best_match_distance = distance

                                    # Replace missing values from row found
                                    self._df.loc[index, column] = weather_data_columns_slices[column].loc[best_match_index, column]

                    if merge_log is not None:
                        del merge_log

            # Calculate next date interval starting from start of next month
            iteration_start_date = datetime.datetime(year=iteration_end_date.year + int(iteration_end_date.month / 12),
                                                     month=iteration_end_date.month % 12 + 1,
                                                     day=1)
            iteration_end_date = end_date

            if iteration_log is not None:
                del iteration_log

    def extract_from_csv(self, csv_file_path: str, allow_nan_rows: bool=False) -> None:
        '''Extract HAB data from CSV file and stores it in internal dataframe.
        
        Parameters:
        csv_file_path: File path of CSV file.
        allow_nan_rows: Weather to include rows in missing values.'''
        # Load data from files
        self._df = pd.read_csv(filepath_or_buffer=csv_file_path,
                              usecols=HABDataETLHelper._api_columns)

        # Convert data types
        for column_index in range(len(HABDataETLHelper._api_columns)):
            self._df[HABDataETLHelper._api_columns[column_index]] = self._df[HABDataETLHelper._api_columns[column_index]].astype(HABDataETLHelper._api_datatypes[column_index])

        # Drop rows with missing data, if requested
        if not allow_nan_rows:
            self._df.dropna(inplace=True)

    def save_to_csv(self, csv_file_name: str) -> None:
        '''Saves internal dataframe to a CSV file.'''
        self._df.to_csv(csv_file_name, index=False, na_rep='NULL')

    def _GetLogger(self, message: str):
        if self._logger is not None:
            return self._logger.get_log_token(message)
        return None


class WeatherDataETLHelper:
    _columns = ['DATE', 'LONGITUDE', 'LATITUDE']
    _datatypes = [None, np.float64, np.float64]

    def __init__(self, logger: ETLLogger=None):
        self._df = None
        self._logger = logger

    def get_dataframe(self) -> pd.DataFrame:
        '''Returns internal dataframe.'''
        return self._df

    def run_et_from_api(self, start_date: datetime.datetime, end_date: datetime.datetime, columns: list[str],
                        datatypes: list[np.dtype], bounding_box: list[float]):
        '''Run extraction and transformation using the NOAA API as the
        data source and an internal dataframe as the data sink.

        Parameters:
        start_date: Start sample date for extraction, inclusive.
        end_date: End sample date for extraction, inclusive.
        columns: Names of columns to query from weather data.
        datatypes: Datatypes of columns in same order as the "columns"
        parameter.
        bounding_box: Bounding box for query in order of
        NW (lat, long), SE (lat, long).
        '''
        self.transform_from_api(
            json_data=self.extract_from_api(start_date=start_date,
                                            end_date=end_date,
                                            columns=columns,
                                            bounding_box=bounding_box),
            columns=columns,
            datatypes=datatypes)

    def extract_from_api(self, start_date: datetime.datetime, end_date: datetime.datetime, columns: list[str],
                         bounding_box: list[float]):
        '''Extracts weather data from NOAA API. Returns extracted JSON
        data.
        
        Parameters:
        start_date: Start sample date for extraction.
        end_date: End sample date for extraction, inclusive.
        columns: Names of columns to query from weather data.
        bounding_box: Bounding box for query in order of
        NW (lat, long), SE (lat, long).'''
        log = self._GetLogger('Extracting weather data from API')

        # Convert to string
        bounding_box_str = []
        for value in bounding_box:
            bounding_box_str.append(str(value))

        # Request from NOAA API
        response = urllib3.request(method='GET',
                                   url='https://www.ncei.noaa.gov/access/services/data/v1',
                                   timeout=300.0,  # Allow 5 minutes due to large data volume
                                   fields={ 'dataset': 'global-marine',
                                            'boundingBox': ','.join(bounding_box_str),
                                            'format': 'json',
                                            'startDate': start_date.strftime('%Y-%m-%d'),
                                            'endDate': end_date.strftime('%Y-%m-%d'),
                                            'dataTypes': ','.join(columns) })

        if response.status == 200:
            # Convert to JSON. Throws expection for invalid JSON.
            return response.json()
        else:
            raise Exception(f'HTTP request failed. Status: {response.status}')

    def transform_from_api(self, json_data: dict, columns: list[str], datatypes: list[np.dtype]) -> None:
        '''Transforms JSON data from NOAA API and stores it into
        internal dataframe.
        
        Parameters:
        json_data: JSON data extracted from NOAA API.
        columns: Names of columns to transform.
        datatypes: Datatypes of columns in same order as the "columns"
        parameter.
        '''
        log = self._GetLogger('Transforming weather data from API')

        # JSON dictionary accesses will throw an exception if JSON keys are not as expected. This is OK.
        transformed_data = {}

        for column in WeatherDataETLHelper._columns:
            transformed_data[column] = []

        for column in columns:
            transformed_data[column] = []

        # Extract data into format for dataframe
        for row_index in range(len(json_data)):
            for column in transformed_data.keys():
                try:
                    transformed_data[column].append(json_data[row_index][column])
                except KeyError:
                    # Some rows may be missing some columns, so append NaN
                    transformed_data[column].append(np.nan)

        # # Special case: Convert ISO timestamp to datetime.
        for row_index in range(len(transformed_data['DATE'])):
            transformed_data['DATE'][row_index] = datetime.datetime.fromisoformat(transformed_data['DATE'][row_index])

        transformed_data = pd.DataFrame(transformed_data)

        # Convert column data types
        all_columns = WeatherDataETLHelper._columns + columns
        all_datatypes = WeatherDataETLHelper._datatypes + datatypes

        for column_index in range(len(all_columns)):
            # Skip None data types (i.e., do not convert)
            if all_datatypes[column_index] is not None:
                transformed_data[all_columns[column_index]] = transformed_data[all_columns[column_index]].astype(all_datatypes[column_index])

        # Assign dataframe if successful (i.e., no exceptions thrown). Convert data types first as they are all strings in JSON data.
        self._df = transformed_data

    def save_to_csv(self, csv_file_name: str) -> None:
        '''Saves internal dataframe to a CSV file.'''
        self._df.to_csv(csv_file_name)

    def _GetLogger(self, message: str):
        if self._logger is not None:
            return self._logger.get_log_token(message)
        return None


class WeatherForecastDataETLHelper:
    def __init__(self, database_table_name: str, logger: ETLLogger=None):
        self._df = None
        self._database_table_name = database_table_name
        self._logger = logger

    def get_dataframe(self) -> pd.DataFrame:
        '''Returns internal dataframe.'''
        return self._df

    def run_etl_from_api(self, start_date: datetime.datetime, latitudes: list[float],
                         longitudes: list[float], latlong_delta: float,
                         min_date_resolution: datetime.timedelta) -> None:
        self.transform_from_api(
            dataset_proxy=self.extract_from_api(date=start_date),
            start_date=start_date,
            latitudes=latitudes,
            longitudes=longitudes,
            latlong_delta=latlong_delta,
            min_date_resolution=min_date_resolution)
        self.load_to_database()

    def extract_from_api(self, date: datetime.datetime):
        '''Extracts weather data from NOAA NGOFS2 forecast dataset API.
        Returns DAP2 dataset proxy.
        
        Parameters:
        date: Nearest date to extract forecasted data from.'''
        # Extract NOAA NGOFS2 forecast dataset from THREDDS server
        # using DAP2 protocol. DAP endpoint URL format is the
        # following:
        # <base_url>/<year>/<month>/<day>/<base_filename>.<year><month><day>.t<cycle>z.nc
        #
        # The forecast is performed every 6 hours each day, each
        # being 2-days long. Cycles are labeled as 3, 9, 15, or 21. It
        # is assumed that each is at the center of a 6-hour interval.
        #
        # Example URL: https://opendap.co-ops.nos.noaa.gov/thredds/dodsC/NOAA/NGOFS2/MODELS/2024/03/23/nos.ngofs2.stations.forecast.20240323.t15z.nc
        log = self._GetLogger('Extracting weather forecast data from API')

        # Calculate cycle
        file_date = datetime.datetime(year=date.year,
                                      month=date.month,
                                      day=date.day,
                                      hour=(3 + 6 * (date.hour // 6)))

        # Reattempt data request for previous cycles until 2 days. Beyond two days,
        # no future values would be present since the forecast period is for 2 days.
        while date - file_date <= datetime.timedelta(days=2.0):
            try:
                # Request dataset proxy from API. Accesses to this proxy will download the data.
                return pydapclient.open_url(url=f'https://opendap.co-ops.nos.noaa.gov/thredds/dodsC/NOAA/NGOFS2/MODELS/{file_date.year:04}/{file_date.month:02}/{file_date.day:02}/nos.ngofs2.stations.forecast.{file_date.year:04}{file_date.month:02}{file_date.day:02}.t{file_date.hour:02}z.nc')
            except Exception:
                # Try again for previous cycle
                file_date -= datetime.timedelta(hours=6.0)

    def transform_from_api(self, dataset_proxy, start_date: datetime.datetime, latitudes: list[float], longitudes: list[float],
                           latlong_delta: float, min_date_resolution: datetime.timedelta) -> None:
        '''Transforms data extracted from NOAA NGOFS2 forecast dataset
        and stores it into internal dataframe.

        Parameters:
        dataset_proxy: DAP2 proxy for weather forecast dataset.
        start_date: Start date for weather forecast, inclusive.
        latitudes: Latitudes in [-180, 180) degrees.
        longitudes: Longitudes in [-180, 180) degrees.
        latlong_delta: Maximum difference between HAB and weather
        forecast data latitude and longitude.
        min_date_resolution: Minimum time resolution for weather
        forecast data. Default is 4 hours.'''
        log = self._GetLogger('Transforming weather forecast data from API')

        transformed_data = {'DATETIME': [],
                            'LATITUDE': [],
                            'LONGITUDE': [],
                            'WATER_TEMP': [],
                            'SALINITY': [],
                            'WIND_SPEED': [],
                            'WIND_DIR': []}

        # Download data. Data structure:
        #   [station_index] for location data.
        #   [time_index] for time data.
        #   [time_index][sigma_layer][station_index] for water
        #   temperature and salinity. Take data from first sigma
        #   layer.
        #   [time_index][station_index] for wind velocities
        #   Location data index is station index.
        #   Time data index is time index.
        lat_data = dataset_proxy['lat'][:].data
        lon_data = dataset_proxy['lon'][:].data
        time_data = dataset_proxy['time'][:].data
        salinity_data = dataset_proxy['salinity'][:].data
        water_temp_data = dataset_proxy['temp'][:].data
        eastward_wind_velocity_data = dataset_proxy['uwind_speed'][:].data
        northward_wind_velocity_data = dataset_proxy['vwind_speed'][:].data

        for location_index in range(len(latitudes)):
            # Convert [0, 360) degrees to [0, 2*pi) radian
            latitude_radian = 2 * np.pi * latitudes[location_index] / 360.0
            longitude_radian = 2 * np.pi * longitudes[location_index] / 360.0

            # Find closest station within delta
            closest_station_index = None
            min_distance = None

            for station_index in range(len(lat_data)):
                # Only consider locations within delta. Convert station latitude and longitude
                # from [0, 360) degrees to [-180, 180) degrees for equal formats.
                if (abs(latitudes[location_index] - (lat_data[station_index] if lat_data[station_index] < 180.0 else lat_data[station_index] - 360.0)) <= latlong_delta
                    and abs(longitudes[location_index] - (lon_data[station_index] if lon_data[station_index] < 180.0 else lon_data[station_index] - 360.0)) <= latlong_delta):
                    # Convert [0, 360) degrees to [0, 2*pi) radian
                    station_latitude_radian = 2 * np.pi * lat_data[station_index] / 360.0
                    station_longitude_radian = 2 * np.pi * lon_data[station_index] / 360.0

                    # Calculate distance between lat-long points using
                    # haversine formula for a cental angle
                    distance = (12742 * np.arcsin(np.sqrt((np.sin(station_latitude_radian - latitude_radian) ** 2)) / 2.0
                                + np.cos(latitude_radian) * np.cos(station_latitude_radian) * np.sin((station_longitude_radian - longitude_radian) / 2.0) ** 2.0))

                    if min_distance is None or distance < min_distance:
                        closest_station_index = station_index
                        min_distance = distance

            # Transform data if a station within delta is found
            if closest_station_index is not None:
                last_datetime = None

                for time_index in range(len(time_data)):
                    # Convert date from days since 2019-01-01 00:00:00
                    converted_time = datetime.datetime(year=2019, month=1, day=1) + datetime.timedelta(days=float(time_data[time_index]))

                    # Only insert data for a given time resolution. Assumes that data from API is in ascending time order.
                    if converted_time >= start_date and (last_datetime is None or converted_time - last_datetime >= min_date_resolution):
                        last_datetime = converted_time
                        transformed_data['DATETIME'].append(converted_time)

                        # Convert latitude and longitude from [0, 360) degrees to [-180, 180) degrees
                        transformed_data['LATITUDE'].append(latitudes[location_index] if latitudes[location_index] < 180.0 else latitudes[location_index] - 360.0)
                        transformed_data['LONGITUDE'].append(longitudes[location_index] if longitudes[location_index] < 180.0 else longitudes[location_index] - 360.0)

                        # Water temperature is in Centigrade and salinity is in ppt. Use first sigma layer.
                        transformed_data['WATER_TEMP'].append(water_temp_data[time_index][0][closest_station_index])
                        transformed_data['SALINITY'].append(salinity_data[time_index][0][closest_station_index])

                        # Convert eastward and northward wind speeds in m/s to wind speed in mpg and direction in degrees
                        transformed_data['WIND_SPEED'].append(np.sqrt(eastward_wind_velocity_data[time_index][closest_station_index] ** 2 + northward_wind_velocity_data[time_index][closest_station_index] ** 2) / 1609.344 * 3600.0)
                        try:
                            # Convert [-180, 180) degrees to [0, 360) degrees
                            transformed_data['WIND_DIR'].append(np.arctan(northward_wind_velocity_data[time_index][closest_station_index] / eastward_wind_velocity_data[time_index][closest_station_index]) / (2.0 * np.pi) * 360.0)

                            if transformed_data['WIND_DIR'][-1] < 0.0:
                                transformed_data['WIND_DIR'][-1] += 360.0
                        except ZeroDivisionError:
                            # Handle case of 0 eastward wind speed (90 or 270 degrees)
                            transformed_data['WIND_DIR'].append(90.0 if northward_wind_velocity_data[time_index][closest_station_index] >= 0.0 else 270.0)

        self._df = pd.DataFrame(transformed_data)

    def load_to_database(self) -> None:
        '''Loads dataframe to MySQL database.'''
        log = self._GetLogger('Loading weather forecast data to database')

        # Connect to database
        db = MySQLdb.connect(host=DATABASES['default']['HOST'],
                             port=int(DATABASES['default']['PORT']),
                             database=DATABASES['default']['NAME'],
                             user=DATABASES['default']['USER'],
                             password=DATABASES['default']['PASSWORD'])
        db_cursor = db.cursor()

        # Optimize insert by using a parametrized query and call executemany
        query = f'INSERT INTO {self._database_table_name}({",".join(self._df.keys())}) VALUES ({",".join(["%s"] * len(self._df.keys()))})'

        # Insert rows
        query_values = []
        for row_index in self._df.index:
            row_values = []

            for column_index in range(len(self._df.keys())):
                if self._df.keys()[column_index] == 'DATETIME':
                    row_values.append(f'{self._df[self._df.keys()[column_index]][row_index].strftime("%Y-%m-%d %H:%M:%S")}')
                elif pd.isnull(self._df[self._df.keys()[column_index]][row_index]):
                    row_values.append(None)
                else:
                    row_values.append(str(self._df[self._df.keys()[column_index]][row_index]))

            query_values.append(row_values)

        db_cursor.executemany(query, query_values)

        db.commit()
        db.close()

    def _GetLogger(self, message: str):
        if self._logger is not None:
            return self._logger.get_log_token(message)
        return None


class ETLManager:
    def __init__(self, enable_logging: bool=False, log_file_dir: str=None, use_test_db: bool=False):
        self._hab_database_table_name = 'habsos_j_test' if use_test_db else 'habsos_j'
        self._forecast_database_table_name = 'forecast_j_test' if use_test_db else 'forecast_j'
        if enable_logging:
            self._logger = ETLLogger(log_file_dir=log_file_dir)
        else:
            self._logger = None

    def run_etl(self, start_date: datetime.datetime=None, end_date: datetime.datetime=None,
                supplement_from_weather_data: bool=True, date_delta: float=datetime.timedelta(days=1.0),
                latlong_delta: float=0.1, min_forecast_date_resolution: datetime.timedelta=datetime.timedelta(hours=4.0),
                chunk_size_days: int=180, allow_missing_rows: bool=False,
                skip_hab_etl: bool=False, skip_weather_forecast_etl: bool=False):
        '''Runs complete ETL for HAB and weather forecast data.

        Parameters:
        start_date: Start sample date for extraction, inclusive. If
        None, then the latest time in the database is used, exclusive.
        Default is None.
        end_date: End sample date for extraction, inclusive. If None,
        then the current time is used. Default is None.
        supplement_from_weather_data: Whether to supplement missing
        data from different weather datasets. Default is True.
        date_delta: Maximum difference between HAB and weather data
        sample dates for merging. Default is 1 day.
        latlong_delta: Maximum difference between HAB and weather
        data latitude and longitude for merging. Default is 0.1.
        min_forecast_date_resolution: Minimum time resolution for
        weather forecast data. Default is 4 hours.
        chunk_size_days: Time interval size in days to perform each ETL
        operation in. Default is 180.
        allow_nan_rows: Whether to allow rows with missing values to be
        loaded into the MySQL database. Default is False.
        skip_hab_etl: Whether to skip ETL for HAB data. Default is
        False.
        skip_weather_forecast_etl: Whether to skip ETL for weather
        forecast data. Default is False.'''
        # If start date is not specified, then use latest timestamp
        # from database (exclusive)
        start_date_exclusive = False

        if start_date == None:
            start_date = ETLManager._get_latest_sample_date_from_database(self._hab_database_table_name)
            start_date_exclusive = True

        # If end date is not specified, then use current time
        if end_date == None:
            end_date = datetime.datetime.now()

        # TODO: Fix this bug. If database is empty, then start_date is
        # always None unless set in argument. For now, set to 1953-01-01.
        if start_date is None:
            start_date = datetime.datetime(year=1953, month=1, day=1)

        # Run ETL for HAB data, if not skipped
        if not skip_hab_etl:
            chunk_start_date = start_date
            chunk_end_date = end_date

            while chunk_start_date < end_date:
                # Limit ETL interval within chunk size
                if chunk_end_date - chunk_start_date > datetime.timedelta(days=chunk_size_days):
                    chunk_end_date = chunk_start_date + datetime.timedelta(days=chunk_size_days)

                # Chunks after first must have exclusive start date to
                # prevent duplicating data from end of previous chunk
                if start_date != chunk_start_date:
                    start_date_exclusive = True

                if self._logger is not None:
                    log = self._logger.get_log_token(f'Running ETL for {chunk_start_date.isoformat()} to {chunk_end_date.isoformat()}')

                # Run ETL in chunks to prevent system from running out of
                # memory for very large requests
                hab_data = HABDataETLHelper(database_table_name=self._hab_database_table_name, logger=self._logger)
                hab_data.run_etl_from_api(start_date=chunk_start_date,
                                        end_date=chunk_end_date,
                                        start_date_exclusive=start_date_exclusive,
                                        supplement_from_weather_data=supplement_from_weather_data,
                                        date_delta=date_delta,
                                        latlong_delta=latlong_delta,
                                        allow_nan_rows=allow_missing_rows)

                if self._logger is not None:
                    del log

                # Calculate next date interval starting from start of next month
                chunk_start_date = chunk_end_date
                chunk_end_date = end_date

        # Run ETL for weather forecast data, if not skipped. Use end date for the forecast dataset.
        if not skip_weather_forecast_etl:
            weather_forecast_data = WeatherForecastDataETLHelper(database_table_name=self._forecast_database_table_name,
                                                                 logger=self._logger)

            # Get all distinct (latitude, longitude) locations in HAB database
            latitudes, longitudes = self._get_distinct_locations_from_hab_database()

            # Clear old forecast data first
            self.clear_forecast_database()

            weather_forecast_data.run_etl_from_api(start_date=end_date,
                                                   latitudes=latitudes,
                                                   longitudes=longitudes,
                                                   latlong_delta=latlong_delta,
                                                   min_date_resolution=min_forecast_date_resolution)

    def clear_hab_database(self):
        '''Deletes all rows from the HAB database table.'''
        if self._logger is not None:
            log = self._logger.get_log_token('Clearing HAB database')
        self._clear_database(self._hab_database_table_name)

    def clear_forecast_database(self):
        '''Deletes all rows from the weather forecast database table.'''
        if self._logger is not None:
            log = self._logger.get_log_token('Clearing weather forecast database')
        self._clear_database(self._forecast_database_table_name)

    def _clear_database(self, database_table_name: str):
        # Connect to database
        db = MySQLdb.connect(host=DATABASES['default']['HOST'],
                             port=int(DATABASES['default']['PORT']),
                             database=DATABASES['default']['NAME'],
                             user=DATABASES['default']['USER'],
                             password=DATABASES['default']['PASSWORD'])
        db_cursor = db.cursor()

        # Delete every row in database
        db_cursor.execute(f'DELETE FROM {database_table_name}')
        db.commit()
        db.close()

    def _get_latest_sample_date_from_database(database_table_name: str) -> datetime.datetime:
        '''Returns most recent sample date in MySQL database.

        Parameters:
        database_table_name: Name of MySQL database table.'''
        # Connect to database
        db = MySQLdb.connect(host=DATABASES['default']['HOST'],
                             port=int(DATABASES['default']['PORT']),
                             database=DATABASES['default']['NAME'],
                             user=DATABASES['default']['USER'],
                             password=DATABASES['default']['PASSWORD'])
        db_cursor = db.cursor()

        # Query for latest timestamp
        db_cursor.execute(f'SELECT SAMPLE_DATETIME FROM {database_table_name} ORDER BY SAMPLE_DATETIME DESC LIMIT 1')

        sample_date = None

        row = db_cursor.fetchone()
        if row is not None:
            sample_date = row[0]

        db.close()

        return sample_date

    def _get_earliest_sample_date_from_database(database_table_name: str) -> datetime.datetime:
        '''Returns the oldest sample date in MySQL database.

        Parameters:
        database_table_name: Name of MySQL database table.'''
        # Connect to database
        db = MySQLdb.connect(host=DATABASES['default']['HOST'],
                             port=int(DATABASES['default']['PORT']),
                             database=DATABASES['default']['NAME'],
                             user=DATABASES['default']['USER'],
                             password=DATABASES['default']['PASSWORD'])
        db_cursor = db.cursor()

        # Query for oldest timestamp
        db_cursor.execute(f'SELECT SAMPLE_DATETIME FROM {database_table_name} ORDER BY SAMPLE_DATETIME ASC LIMIT 1')

        sample_date = None

        row = db_cursor.fetchone()
        if row is not None:
            sample_date = row[0]

        db.close()

        return sample_date

    def _get_distinct_locations_from_hab_database(self) -> list[list[float], list[float]]:
        '''Returns all disticts locations in HAB database in
        [latitude, longitude].'''
        # Connect to database
        db = MySQLdb.connect(host=DATABASES['default']['HOST'],
                             port=int(DATABASES['default']['PORT']),
                             database=DATABASES['default']['NAME'],
                             user=DATABASES['default']['USER'],
                             password=DATABASES['default']['PASSWORD'])
        db_cursor = db.cursor()

        # Query for oldest timestamp
        db_cursor.execute(f'SELECT DISTINCT LATITUDE, LONGITUDE FROM {self._hab_database_table_name}')

        locations = [[], []]

        row = db_cursor.fetchone()

        while row is not None:
            locations[0].append(row[0])
            locations[1].append(row[1])
            row = db_cursor.fetchone()

        db.close()

        return locations


# If running this file, then perform the automation ETL routine
if __name__ == '__main__':
    start_date = None
    end_date = None

    # Get arguments
    arg_index = 1  # Skip script name
    clear_database = False
    use_test_db = False
    skip_hab_etl = False
    skip_weather_forecast_etl = False

    while arg_index < len(sys.argv):
        if sys.argv[arg_index] == '-cleardb':
            clear_database = True
        elif sys.argv[arg_index] == '-testdb':
            use_test_db = True
        elif sys.argv[arg_index] == '-daterange':
            # If using date range, the following two arguments must be dates in ISO format in order of start date, end_date
            if arg_index < len(sys.argv) - 2:
                arg_index += 1
                start_date = datetime.datetime.fromisoformat(sys.argv[arg_index])
                arg_index += 1
                end_date = datetime.datetime.fromisoformat(sys.argv[arg_index])
            else:
                print(f'Daterange needs 2 date arguments in ISO format.')
                exit(-1)
        elif sys.argv[arg_index] == '-skipforecast':
            skip_weather_forecast_etl = True
        elif sys.argv[arg_index] == '-skiphab':
            skip_hab_etl = True
        else:
            print(f'Argument not recognized: {sys.argv[arg_index]}')
            exit(-1)

        arg_index += 1

    # TODO: Determine a proper log file directory
    mgr = ETLManager(enable_logging=True, log_file_dir='.', use_test_db=use_test_db)

    # Delete data in database, if requested
    if clear_database:
        if not skip_hab_etl:
            mgr.clear_hab_database()

    # Run routine ETL procedure
    mgr.run_etl(start_date=start_date,
                end_date=end_date,
                supplement_from_weather_data=True,
                date_delta=datetime.timedelta(days=1.0),
                latlong_delta=0.2,
                min_forecast_date_resolution=datetime.timedelta(days=1.0),
                chunk_size_days=180,
                allow_missing_rows=True,
                skip_hab_etl=skip_hab_etl,
                skip_weather_forecast_etl=skip_weather_forecast_etl)