import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from common.Database import Database
from NN.Net import Net
from sklearn.metrics import accuracy_score, classification_report


# Load and preprocess data
def load_and_preprocess_data():
    db = Database()
    query = """
        SELECT * 
        FROM habsos_j
        WHERE LATITUDE IS NOT NULL AND LONGITUDE IS NOT NULL
        AND CATEGORY IS NOT NULL
        AND SALINITY IS NOT NULL
        AND WATER_TEMP IS NOT NULL
        and SAMPLE_DATETIME < '2023-01-01 00:00:00';
    """
    records, columns = db.execute_query(query)
    db.close()

    df = pd.DataFrame(records, columns=columns)
    df['date'] = pd.to_datetime(df['SAMPLE_DATETIME'])
    le = LabelEncoder()
    df['category_encoded'] = le.fit_transform(df['CATEGORY'])

    features = ['LATITUDE', 'LONGITUDE', 'SALINITY', 'WATER_TEMP']
    X = df[features]
    y = df['category_encoded']
    return train_test_split(X, y, test_size=0.2, random_state=42), le

# Scale features
def scale_features(X_train, X_test, features_to_scale):
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[features_to_scale] = scaler.fit_transform(X_train[features_to_scale])
    X_test_scaled[features_to_scale] = scaler.transform(X_test[features_to_scale])
    return X_train_scaled, X_test_scaled

# Convert data to tensors and create data loaders
def create_data_loaders(X_train_scaled, X_test_scaled, y_train, y_test, batch_size=64):
    X_train_tensor = torch.tensor(X_train_scaled.values, dtype=torch.float)
    X_test_tensor = torch.tensor(X_test_scaled.values, dtype=torch.float)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.long)
    y_test_tensor = torch.tensor(y_test.values, dtype=torch.long)

    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size)
    return train_loader, test_loader

# Training the model
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=128):
    print('Start training')
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    # Track the best loss
    best_loss = float('inf')
    best_model = None

    for epoch in range(num_epochs):
        model.train()  # Set the model to training mode
        train_loss = 0

        for X_batch, y_batch in train_loader:
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        train_loss /= len(train_loader)


        # Evaluate on the validation set
        model.eval()  # Set the model to evaluation mode
        with torch.no_grad():
            val_loss = 0
            for X_val, y_val in val_loader:
                outputs = model(X_val)
                val_loss += criterion(outputs, y_val).item()
            val_loss /= len(val_loader)
        print(f'Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss:.4f}, Validation Loss: {val_loss:.4f}')

        if val_loss < best_loss:
            best_loss = val_loss
            best_model = model.state_dict()
            torch.save(best_model, 'best_nn_model-0424.pth')  # Save the best model
            print(f'New best model found at epoch {epoch+1}!')


        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, Val Loss: {val_loss:.4f}')

    return best_model

# Evaluate the model
def evaluate_model(test_loader, le, model_path):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    model.load_state_dict(torch.load(model_path))
    model.to(device)

    model.eval()  # Set the model to evaluation mode
    all_predictions = []
    all_labels = []

    with torch.no_grad():
        for X_batch, y_batch in test_loader:
            outputs = model(X_batch)
            _, predicted = torch.max(outputs, 1)
            all_predictions.extend(predicted.cpu().numpy())
            all_labels.extend(y_batch.cpu().numpy())

    print(classification_report(all_labels, all_predictions, target_names=le.classes_))

if __name__ == "__main__":
    d, le = load_and_preprocess_data()
    X_train, X_test, y_train, y_test = d
    features_to_scale = ['SALINITY', 'WATER_TEMP']
    X_train_scaled, X_test_scaled = scale_features(X_train, X_test, features_to_scale)

    train_loader, test_loader = create_data_loaders(X_train_scaled, X_test_scaled, y_train, y_test)

    input_size = 4
    num_classes = 5
    model = Net(input_size,num_classes)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    train_model(model, train_loader, test_loader, criterion, optimizer, num_epochs=120)
    evaluate_model(test_loader, le, model_path="best_nn_model-0424.pth")
