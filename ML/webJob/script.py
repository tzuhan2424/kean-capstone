from Database import Database
import joblib
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting the prediction job...")

    model_filename = 'random_forest_model.joblib'
    scaler_filename = 'scaler.joblib'

    # Load model and scaler
    try:
        model = joblib.load(model_filename)
        scaler = joblib.load(scaler_filename)
        logging.info("Model and scaler loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading model or scaler: {e}")
        return

    # Initialize database connection
    db = Database()

    try:
        # Fetch data
        table_name = 'forecast_j'
        fetch_query = f"""
            SELECT ID, LATITUDE, LONGITUDE, SALINITY, WATER_TEMP, WIND_DIR, WIND_SPEED
            FROM {table_name};
        """
        records, columns = db.execute_query(fetch_query)
        if records:
            logging.info("Data fetched successfully from the database.")
        else:
            logging.warning("No data fetched from the database. Check the query or database status.")

        df = pd.DataFrame(records, columns=columns)

        # Data preprocessing
        features = ['LATITUDE', 'LONGITUDE', 'SALINITY', 'WATER_TEMP', 'WIND_DIR', 'WIND_SPEED']
        X_predict = scaler.transform(df[features])
        logging.debug("Data preprocessing completed.")

        # Prediction
        predictions = model.predict(X_predict)
        logging.info("Predictions made successfully.")

        # Update the database
        db.update_predictions(table_name, predictions, df['ID'])
        logging.info("Database updated with new predictions.")
    
    except Exception as e:
        logging.error(f"An error occurred during the prediction process: {e}")
    finally:
        # Ensure the database connection is closed properly
        db.close()
        logging.info("Database connection closed.")

if __name__ == '__main__':
    main()
