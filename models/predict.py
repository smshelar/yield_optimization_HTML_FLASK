import joblib
import pandas as pd

model = joblib.load('models/yield_model.pkl')


def predict_yield(data):

    input_df = pd.DataFrame([data])

    prediction = model.predict(input_df)[0]

    return round(prediction, 2)