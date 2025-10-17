import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Lokasi file ini
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')     # app/models
pathModel = os.path.join(MODEL_DIR, 'Random_Forest_Failure_Detection.pkl')
pathScaler = os.path.join(MODEL_DIR, 'StandardScaler_v1.pkl')
model = joblib.load(pathModel)
scaler = joblib.load(pathScaler)

def predict_failure(df_input: pd.DataFrame):
    scaled_feature = scaler.transform(df_input)
    prediction = model.predict(scaled_feature)
    failure_result = bool(prediction[0])
    return failure_result