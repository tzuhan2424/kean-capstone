import sys
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
ml_directory = os.path.dirname(script_directory)
if ml_directory not in sys.path:
    sys.path.insert(0, ml_directory)
    
from common.Database import Database

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import numpy as np
from sklearn.preprocessing import StandardScaler


# Example usage
if __name__ == "__main__":
    db = Database()
    query = """
        select * 
        FROM habsos_j
        WHERE LATITUDE IS NOT NULL and LONGITUDE IS NOT NULL
        AND SAMPLE_DATE  IS NOT NULL
        and CATEGORY  is not NULL
        and SALINITY  is not NULL
        and WATER_TEMP is not null
        and WIND_DIR is not null 
        and WIND_SPEED is not null;
    """
    records, columns = db.execute_query(query)
    db.close()
    df = pd.DataFrame(records, columns=columns)
    df['date'] = pd.to_datetime(df['SAMPLE_DATETIME'])
    df['month'] = df['date'].dt.month
    le = LabelEncoder()
    df['category_encoded'] = le.fit_transform(df['CATEGORY'])





    

    features = ['LATITUDE', 'LONGITUDE', 'SALINITY', 'WATER_TEMP', 'WIND_DIR', 'WIND_SPEED']
    '''
      example data:
      SALINITY: 32.00
      WATER_TEMP: 28
      WIN_DIR: 135
      WIND_SPEED: 5
    '''


    X = df[features]
    y = df['category_encoded']



    features_to_scale = ['SALINITY', 'WATER_TEMP', 'WIND_DIR', 'WIND_SPEED']
    X_to_scale = X[features_to_scale]



    X_train, X_test, y_train, y_test = train_test_split(X[features], y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[features_to_scale] = scaler.fit_transform(X_train[features_to_scale])
    X_test_scaled[features_to_scale] = scaler.transform(X_test[features_to_scale])

    # model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=8000, class_weight='balanced') #this seem good
    


    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    # Print accuracy and classification report using original labels
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=le.classes_))



