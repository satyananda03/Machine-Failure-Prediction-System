import uuid
from app.schemas.db_schema import MachineLogs
from app.database.firestore_db import db

async def add_machine_data(data: MachineLogs):
    doc_ref = db.collection("machine_logs").document(str(uuid.uuid4()))
    doc_ref.set(data.dict())
    return {"message": "Data added successfully."}

from google.cloud.firestore_v1 import DocumentSnapshot

async def read_all_data():
    docs = db.collection("machine_logs").stream()
    all_data = []
    for doc in docs:
        data = doc.to_dict()
        if "timestamp" in data:
            data["timestamp"] = data["timestamp"].isoformat()  # convert to str (convert again into datetime later in streamlit)
        all_data.append(data)
    return all_data