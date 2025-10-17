from app.database.crud import read_all_data
from fastapi import APIRouter
from typing import List
from app.schemas.db_schema import MachineLogs

machine_logs_routes = APIRouter()

@machine_logs_routes.get("/machine-logs", response_model=List[MachineLogs])
async def get_machine_data():
    all_data = await read_all_data()
    return all_data