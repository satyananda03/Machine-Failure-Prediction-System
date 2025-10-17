import pandas as pd
from datetime import datetime
from fastapi import APIRouter
from app.services.failure_classifier import clasify_failure
from app.services.failure_predictor import predict_failure
from app.schemas.predict_schema import PredictRequest, PredictResponse
from app.schemas.db_schema import MachineLogs
from app.database.crud import add_machine_data

predict_routes = APIRouter()

@predict_routes.post("/predict", response_model=PredictResponse)
async def predict(request_data: PredictRequest):
    timestamp = datetime.now()
    df_input = pd.DataFrame([{'Air Temperature': request_data.air_temperature,
                            'Process Temperature': request_data.process_temperature,
                            'Rotational Speed': request_data.rotational_speed,
                            'Torque': request_data.torque,
                            'Tool Wear': request_data.tool_wear
                            }])
    failure_result = predict_failure(df_input)
    if failure_result == True:
        failure_TWF, failure_HDF, failure_PWF, failure_OSF, failure_RNF = clasify_failure(df_input)
    else :
        failure_TWF = failure_HDF = failure_PWF = failure_OSF = failure_RNF = False
    # Store data to Database
    machine_log = MachineLogs(timestamp=timestamp,
                            machine_id=request_data.machine_id,
                            machine_type=request_data.machine_type,
                            torque=request_data.torque,
                            air_temperature=request_data.air_temperature,
                            rotational_speed=request_data.rotational_speed,
                            process_temperature=request_data.process_temperature,
                            tool_wear=request_data.tool_wear,
                            failure_status=failure_result,
                            failure_type_twf=failure_TWF,
                            failure_type_hdf=failure_HDF,
                            failure_type_pwf=failure_PWF,
                            failure_type_osf=failure_OSF,
                            failure_type_rnf=failure_RNF)
    await add_machine_data(machine_log)
    # Respons JSON
    response_data = {
        "failure_status": failure_result,
        "failure_type_twf": failure_TWF,
        "failure_type_hdf": failure_HDF,
        "failure_type_pwf": failure_PWF,
        "failure_type_osf": failure_OSF,
        "failure_type_rnf": failure_RNF
        }
    return PredictResponse(**response_data)