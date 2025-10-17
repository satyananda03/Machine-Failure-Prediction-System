import pandas as pd
import os
import joblib
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Lokasi file ini
MODEL_DIR = os.path.join(BASE_DIR, '..', 'models')     # app/models
pathModel = os.path.join(MODEL_DIR, 'SVM_Failure_Type_Classification.pkl')
pathScaler = os.path.join(MODEL_DIR, 'StandardScaler_v2.pkl')
model = joblib.load(pathModel)
scaler = joblib.load(pathScaler)

def clasify_failure(df_input: pd.DataFrame):
    scaled_feature = scaler.transform(df_input)
    prediction = model.predict(scaled_feature) # Output : np.array([[0,1,0,0,0]])
    failure_TWF = bool(prediction[0][0])
    failure_HDF = bool(prediction[0][1])
    failure_PWF = bool(prediction[0][2])
    failure_OSF = bool(prediction[0][3])
    failure_RNF = bool(prediction[0][4])
    return failure_TWF, failure_HDF, failure_PWF, failure_OSF, failure_RNF