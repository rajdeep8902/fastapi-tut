from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City of the patient")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal["Male", "Female", "Others"], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in cm")]
    weight: Annotated[float, Field(..., description="Weight of the patient in kg")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round((self.weight*10000)/(self.height**2),2)
        return bmi
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
            return "Obese"
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description="Name of the patient")]
    city: Annotated[Optional[str], Field(default=None, description="City of the patient")]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Optional[Literal["Male", "Female", "Others"]], Field(default=None, description="Gender of the patient")]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="Height of the patient in cm")]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description="Weight of the patient in kg")]
    

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f) 
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

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

@app.post("/create")
def create_patient(patient: Patient):
    #load existing data
    data = load_data()
    
    #check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exist")
    
    #add the new patient to the database
    data[patient.id] = patient.model_dump(exclude=["id"])
    
    #save into the json file
    save_data(data)
    
    return JSONResponse(status_code=201, content="Patient created successfully")

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    #load existing data
    data = load_data()
    
    #check if the patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    #updating the patient
    existing_patient = data[patient_id]
    updated_patient = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_patient.items():
        existing_patient[key] = value
    
    #existing_patient -> pydantic obj -> updated bmi + verdict -> pydantic obj -> dict
    existing_patient["id"] = patient_id
    patient_pydantic = Patient(**existing_patient)
    
    #add the modified patient to the database
    data[patient_id] = patient_pydantic.model_dump(exclude=["id"])
    save_data(data)
    return JSONResponse(status_code=200, content="Patient updated successfully")
    