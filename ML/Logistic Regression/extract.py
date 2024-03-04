import sys
sys.path.append('..')  # Adjust path so the common module can be found
from common.Database import Database
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

from sklearn.preprocessing import StandardScaler


# Example usage
if __name__ == "__main__":
    db = Database()
    query = """
        select * 
        FROM habsos_t
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


    features = ['LATITUDE', 'LONGITUDE', 'SALINITY', 'WATER_TEMP', 'WIND_DIR', 'WIND_SPEED', 'month']
    X = df[features]
    y = df['category_encoded']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    model.fit(X_train_scaled, y_train)



    model.fit(X_train, y_train)


    y_pred = model.predict(X_test_scaled)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))

