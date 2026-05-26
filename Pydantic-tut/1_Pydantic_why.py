from pydantic import BaseModel
from typing import List, Dict

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    allergies: List[str]
    contact: Dict[str, str]
    
patient_info = {
    "name": "Nitish", 
    "age": 30,
    "weight": 75.2,
    "allergies": ["pollen", "dust"],
    "contact": {
        "email": "abc@gmail.com",
        "ph_no": "7864016477" 
        }
    }
patient1= Patient(**patient_info)

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient1.allergies)

insert_patient(patient1)