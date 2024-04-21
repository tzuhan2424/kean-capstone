
from common.Database import Database
import joblib
import pandas as pd



if __name__ == '__main__':
    
    model_filename = 'random_forest_model.joblib'
    model = joblib.load(model_filename)
    table_name = 'forecast_j'


    db = Database()
    fetch_query = f"""
        SELECT ID, LATITUDE, LONGITUDE, SALINITY, WATER_TEMP, WIND_DIR, WIND_SPEED
        FROM {table_name};
    """
    records, columns = db.execute_query(fetch_query)
    df = pd.DataFrame(records, columns=columns)
    features = ['LATITUDE', 'LONGITUDE', 'SALINITY', 'WATER_TEMP', 'WIND_DIR', 'WIND_SPEED']
    

    scaler_filename = 'scaler.joblib'
    scaler = joblib.load(scaler_filename)
    X_predict = scaler.transform(df[features])
    # Make predictions
    predictions = model.predict(X_predict)
    # Update the database with the new predictions
    db.update_predictions(table_name, predictions, df['ID'])

    db.close()






