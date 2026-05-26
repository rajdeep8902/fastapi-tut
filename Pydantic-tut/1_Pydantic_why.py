from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional

class Patient(BaseModel):
    name: str
    age: int = Field(gt=0, lt=200)
    weight: float
    allergies: Optional[List[str]] = None
    email: EmailStr
    linkedin_url: AnyUrl
    
patient_info = {
    "name": "Nitish",  
    "age": -30,
    "weight": 75.2,
    # "allergies": ["pollen", "dust"],
    "email": "abc@gmail.com",
    "linkedin_url": "https://linkedin.com/1322"
    }
patient1= Patient(**patient_info)

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient1.email)

insert_patient(patient1)