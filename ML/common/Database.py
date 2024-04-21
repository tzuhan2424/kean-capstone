from dotenv import load_dotenv
import os
from pathlib import Path
import mysql.connector

class Database:
    def __init__(self):
        # Load environment variables from .env file located in the parent directory
        parent_dir = Path(__file__).resolve().parent.parent
        env_path = parent_dir / '.env'
        load_dotenv(dotenv_path=env_path)

        # Retrieve environment variables
        DB_HOST = os.getenv('HOST')
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_NAME = os.getenv('DB_NAME')

        # Establish a connection to the database
        self.conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        """Executes a given SQL query and returns the fetched results."""
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        return records, columns
    
    def execute_mockupdata_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def update_predictions(self, table, predictions, ids):
        """Updates the table with the new predictions using the corresponding IDs."""
        update_query = f"UPDATE {table} SET PREDICT_CATEGORY = %s WHERE ID = %s;"
        # Process updates in batches and log progress
        batch_size = 1000
        for i in range(0, len(predictions), batch_size):
            batch_predictions = predictions[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            update_data = [(int(pred), int(id_)) for pred, id_ in zip(batch_predictions, batch_ids)]
            
            self.cursor.executemany(update_query, update_data)
            self.conn.commit()

            print(f"Updated {i + len(update_data)} rows in {table}")

    def close(self):
        """Closes the cursor and connection."""
        self.cursor.close()
        self.conn.close()
