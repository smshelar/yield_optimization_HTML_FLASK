import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load Data

df = pd.read_csv('data/manufacturing_data.csv')

features = [
    'temperature',
    'pressure',
    'humidity',
    'machine_speed',
    'vibration',
    'raw_material_quality',
    'energy_consumption',
    'downtime_minutes'
]

X = df[features]
y = df['yield_percentage']

# Split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)

print(f'Model MAE: {mae}')

# Save Model

joblib.dump(model, 'models/yield_model.pkl')

print('Model saved successfully')