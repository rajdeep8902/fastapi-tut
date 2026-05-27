from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    allergies: List[str]
    contact: Dict[str, str]
    
    @model_validator(mode="after")
    def validate_emergency(cls, model):
        if model.age > 60 and "emergency" not in model.contact:
            raise ValueError("patients older than 60 must have an emergency contact")
        return model
        
    
patient_info = {
    "name": "Nitish",  
    "age": 70,
    "weight": 75.2,
    "allergies": ["pollen", "dust"],
    "contact":{
        "phone":"1234567890"
    }
}
patient1= Patient(**patient_info)

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.contact)

insert_patient(patient1)