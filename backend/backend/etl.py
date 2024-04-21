import pandas as pd
import urllib3
import datetime
import MySQLdb
from settings import DATABASES

class HABDataETLHelper:
    _columns = ['LATITUDE', 'LONGITUDE', 'SAMPLE_DATE', 'SAMPLE_DEPTH', 'CELLCOUNT', 'SALINITY', 'WATER_TEMP', 'WIND_DIR', 'WIND_SPEED']

    def __init__(self) -> None:
        self._df = None

    def get_dataframe(self) -> pd.DataFrame:
        return self._df

    def run_etl_from_api(self, start_date: datetime=None, end_date: datetime=None) -> None:
        ''' Run extraction, transformation, and loading using the NOAA API as the data source and
        the TideTrack database as the data sink.

        PARAMETERS:
            start_date: Start sample date for extraction, inclusive. If None, then the latest time
                        in the database is used, exclusive. Default is None.
            end_date: End sample date for extraction, inclusive. If None, then the current time is
                      used. Default is None.
        '''
        start_date_exclusive = False

        # If start date is not specified, then use latest timestamp from database (exclusive)
        if start_date == None:
            start_date = self._get_latest_sample_date_from_database()
            start_date_exclusive = True

        # If end date is not specified, then use current time
        if end_date == None:
            end_date = datetime.datetime.now()

        self.transform_from_api(
            self.extract_from_api(start_date=start_date,
                                  end_date=end_date,
                                  start_date_exclusive=start_date_exclusive))
        self.load_to_database_from_api()

    def extract_from_api(self, start_date: datetime, end_date: datetime, start_date_exclusive: bool) -> dict:
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
                                            'outFields': ','.join(HABDataETLHelper._columns),
                                            'returnGeometry': 'false' })

        if response.status == 200:
            # Convert to JSON. Throws expection for invalid JSON.
            return response.json()
        else:
            raise Exception(f'HTTP request failed. Status: {response.status}')

    def transform_from_api(self, json_data: dict) -> None:
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

        # Assign dataframe if successful (i.e., no exceptions thrown)
        self._df = pd.DataFrame(transformed_data)

    def load_to_database_from_api(self) -> None:
        # Connect to database
        db = MySQLdb.connect(host=DATABASES['default']['HOST'],
                             port=int(DATABASES['default']['PORT']),
                             database=DATABASES['default']['NAME'],
                             user=DATABASES['default']['USER'],
                             password=DATABASES['default']['PASSWORD'])
        db_cursor = db.cursor()

        # Table does not allow null values on any column
        df_no_nan = self._df.dropna()

        # Insert rows
        for row_index in df_no_nan.index:
            # Convert from UNIX millisecond timestamp. Due to there being dates before 1970 in the data, this value can be negative.
            query = f'INSERT INTO habsos({",".join(HABDataETLHelper._columns)}) VALUES ('

            for column_index in range(len(HABDataETLHelper._columns)):
                if column_index > 0:
                    query += ','

                if HABDataETLHelper._columns[column_index] == 'SAMPLE_DATE':
                    query += f'"{df_no_nan[HABDataETLHelper._columns[column_index]][row_index].strftime("%Y-%m-%d %H:%M:%S")}"'
                else:
                    query += str(df_no_nan[HABDataETLHelper._columns[column_index]][row_index])

            query += ')'

            db_cursor.execute(query)

        db.commit()
        db.close()

    def extract_from_database(self) -> None:
        # Connect to database
        db = MySQLdb.connect(host=DATABASES['default']['HOST'],
                             port=int(DATABASES['default']['PORT']),
                             database=DATABASES['default']['NAME'],
                             user=DATABASES['default']['USER'],
                             password=DATABASES['default']['PASSWORD'])
        db_cursor = db.cursor()

        # Query for all data
        db_cursor.execute(f'SELECT {",".join(HABDataETLHelper._columns)} FROM habsos')

        data = {}
        for column in HABDataETLHelper._columns:
            data[column] = []

        row = db_cursor.fetchone()
        while row:
            for column_index in range(len(HABDataETLHelper._columns)):
                data[HABDataETLHelper._columns[column_index]].append(row[column_index])

            # Get next row
            row = db_cursor.fetchone()

        self._df = data

    def extract_from_csv(self, csv_file_path: str, allow_nan_rows: bool=False) -> None:
        # Load data from files
        self._df = pd.read_csv(filepath_or_buffer=csv_file_path,
                              usecols=HABDataETLHelper._columns,
                              parse_dates=['SAMPLE_DATE'])

        # Drop rows with missing data, if requested
        if not allow_nan_rows:
            self._df.dropna(inplace=True)

    def save_to_csv(self, csv_file_name: str) -> None:
        self._df.to_csv(csv_file_name)

    def _get_latest_sample_date_from_database(self) -> datetime:
        # Connect to database
        db = MySQLdb.connect(host=DATABASES['default']['HOST'],
                             port=int(DATABASES['default']['PORT']),
                             database=DATABASES['default']['NAME'],
                             user=DATABASES['default']['USER'],
                             password=DATABASES['default']['PASSWORD'])
        db_cursor = db.cursor()

        # Query for latest timestamp
        db_cursor.execute('SELECT SAMPLE_DATE FROM habsos ORDER BY SAMPLE_DATE DESC LIMIT 1')

        sample_date = None

        row = db_cursor.fetchone()
        if row is not None:
            sample_date = db_cursor.fetchone()[0]

        db.close()

        return sample_date