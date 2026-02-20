from fastapi import FastAPI, Path,HTTPException
import json

app = FastAPI()

def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

@app.get("/")
def Hello():
    return {"message": "Hello World I am Mudassar Gill"}

@app.get("/about")
def about():
    return {"message": "I am a student of Computer Science"}

@app.get("/view")
def view():
    return load_data()

# View specific patient by ID
@app.get("/patient/{patient_id}")
def view_patient(patient_id: int = Path(..., description="Patient ID", example=1)):
    data = load_data()
    for patient in data:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")