from fastapi import FastAPI, Path,HTTPException,Query
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
@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description="Sort by age, gender or city"),
    order: str = Query("asc", description="Sorting order: asc or desc", example="asc")
):
    valid_field=["age","gender","city"]
    if sort_by not in valid_field:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by parameter {valid_field}")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400, detail="Invalid order parameter")
    data=load_data()
    sort_order=True if order=="desc" else False
    sorted_data=sorted(data,key=lambda x:x.get(sort_by),reverse=sort_order)
    return sorted_data
    
    