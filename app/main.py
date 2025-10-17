from fastapi import FastAPI
from app.api.endpoints.predict import predict_routes
from app.api.endpoints.machine_logs import machine_logs_routes

app = FastAPI()

app.include_router(predict_routes)
app.include_router(machine_logs_routes)