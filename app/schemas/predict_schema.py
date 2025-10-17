from pydantic import BaseModel

class PredictRequest(BaseModel):
    machine_id: str
    machine_type: str
    torque: float
    air_temperature: float
    rotational_speed: int
    process_temperature: float
    tool_wear: int

class PredictResponse(BaseModel):
    failure_status: bool
    failure_type_twf: bool
    failure_type_hdf: bool
    failure_type_pwf: bool
    failure_type_osf: bool
    failure_type_rnf: bool