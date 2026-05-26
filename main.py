from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f) 
    return data

@app.get("/")
def hello():
    return {"message":"Patient Management System API"}

@app.get("/about")
def about():
    return {"message":"A fully functional API to manage your patient records"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="ID of the patient in the DB", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on basis of height, weight or bmi"), order: str= Query("asc", description="Sort in asc or desc")):
    valid_sort = ["height", "weight", "bmi"]
    valid_order = ["asc", "desc"]
    if sort_by not in valid_sort:
        raise HTTPException(status_code=400, detail=f"Invalid field. Select from {valid_sort}")
    if order not in valid_order:
        raise HTTPException(status_code=400, detail=f"Invalid field. Select from {valid_order}")
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=False if order=="asc" else True)
    return sorted_data
