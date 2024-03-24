from common.Database import Database
import random
from datetime import datetime, timedelta
import mysql.connector
from pathlib import Path
import os

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))

# Mock data generation as before
def generate_mock_data():
    bounding_boxes = [
    { "name": "Area 1", "coordinates": [-96.45, 25.75, -97.73, 27.8] },
    { "name": "Area 2", "coordinates": [-97.73, 27.8, -95.04, 28.85] },
    { "name": "Area 3", "coordinates": [-95.22, 29.85, -91.57, 28.58] },
    { "name": "Area 4", "coordinates": [-91.57, 30.34, -89.24, 28.92] },
    { "name": "Area 5", "coordinates": [-89.24, 30.64, -87, 28.92] },
    { "name": "Area 6", "coordinates": [-87.48, 30.64, -84.88, 29.41] },
    { "name": "Area 7", "coordinates": [-84.95, 30.18, -83.10, 29.01] },
    { "name": "Area 8", "coordinates": [-83.61, 29.01, -82.55, 27.95] },
    { "name": "Area 9", "coordinates": [-83.48, 27.95, -82.11, 26.8] },
    { "name": "Area 10", "coordinates": [-83.34, 26.8, -81.52, 25.89] },
    { "name": "Area 11", "coordinates": [-83.01, 25.89, -79.41, 24.68] },
    { "name": "Area 12", "coordinates": [-81.92, 30.83, -80.62, 29.31] },
    { "name": "Area 13", "coordinates": [-81.04, 29.31, -80.07, 27.53] },
    { "name": "Area 14", "coordinates": [-80.25, 27.53, -79.41, 25.89] }
  ]
  
    start_date = datetime.strptime('2015-10-14', '%Y-%m-%d')
    end_date = datetime.strptime('2015-10-21', '%Y-%m-%d')

    mock_data = []
    for bbox in bounding_boxes:
        for _ in range(100):  #adjust number
            longitude = random.uniform(bbox['coordinates'][2], bbox['coordinates'][0])
            latitude = random.uniform(bbox['coordinates'][1], bbox['coordinates'][3])
            sample_datetime = random_date(start_date, end_date)
            salinity = random.uniform(0, 40)
            water_temp = random.uniform(0, 40)
            wind_dir = random.uniform(0, 365)
            wind_speed = random.uniform(0, 30)
            predict_category = random.randint(0, 4)

            mock_data.append((latitude, longitude, sample_datetime, salinity, water_temp, wind_dir, wind_speed, predict_category))
    return mock_data

def insert_data_into_db(data):
    db = Database()
    query = """
        INSERT INTO habsos_prediction (LATITUDE, LONGITUDE, SAMPLE_DATETIME, SALINITY, WATER_TEMP, WIND_DIR, WIND_SPEED, PREDICT_CATEGORY)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    for record in data:
        db.execute_mockupdata_query(query, record)
    db.close()

# Usage
mock_data = generate_mock_data()
insert_data_into_db(mock_data)