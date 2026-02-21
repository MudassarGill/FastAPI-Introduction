from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, computed_field
from typing import Literal, List
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

# --- Pydantic Patient Model ---
class Patient(BaseModel):
    id: int = Field(..., description="Patient ID", example=1)
    name: str = Field(..., description="Patient Name", example="Mudassar Hussain")
    age: int = Field(..., gt=0, lt=120, description="Patient Age", example=32)
    gender: Literal["Male", "Female", "Other"] = Field(..., description="Patient Gender", example="Male")
    disease: str = Field(..., description="Patient Disease", example="Diabetes Type 2")
    phone: str = Field(..., description="Patient Phone", example="0300-1234567")
    city: str = Field(..., description="Patient City", example="Lahore")
    height: float = Field(..., gt=0, description="Patient Height", example=5.11)
    weight: float = Field(..., gt=0, description="Patient Weight", example=70)

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height * self.height), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"

# --- Helper functions for JSON storage ---
PATIENTS_FILE = "patients.json"

def load_data() -> List[dict]:
    if not os.path.exists(PATIENTS_FILE):
        return []
    with open(PATIENTS_FILE, "r") as file:
        return json.load(file)

def save_data(data: List[dict]):
    with open(PATIENTS_FILE, "w") as file:
        json.dump(data, file, indent=4)

# --- Routes ---

@app.get("/")
def hello():
    return {"message": "Hello World I am Mudassar Gill"}

@app.get("/about")
def about():
    return {"message": "I am a student of Computer Science"}

@app.get("/view")
def view():
    return load_data()

@app.get("/patient/{patient_id}")
def view_patient(patient_id: int = Path(..., description="Patient ID", example=1)):
    data = load_data()
    for patient in data:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort by age, gender or city"),
    order: str = Query("asc", description="Sorting order: asc or desc", example="asc")
):
    valid_fields = ["age", "gender", "city"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by parameter. Must be one of {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order parameter. Must be 'asc' or 'desc'")
    
    data = load_data()
    reverse_order = True if order == "desc" else False
    sorted_data = sorted(data, key=lambda x: x.get(sort_by), reverse=reverse_order)
    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    # Check if patient ID already exists
    if any(p["id"] == patient.id for p in data):
        raise HTTPException(status_code=400, detail="Patient already exists")
    
    # Append new patient
    data.append(patient.model_dump())
    save_data(data)
    return JSONResponse(content={"message": "Patient created successfully"})
    