from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from tensorflow.keras.models import load_model
from utils import preprocess_input
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model("model/lstm_model.keras")

class SensorData(BaseModel):
    data: List[List[float]]

@app.get("/")
def home():
    return {"message": "Predictive Maintenance API Running"}

@app.post("/predict")
def predict(input: SensorData):
    try:
        processed = preprocess_input(input.data)   # ← was input_data.data
        prediction = model.predict(processed)
        return {"predicted_RUL": float(prediction[0][0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))