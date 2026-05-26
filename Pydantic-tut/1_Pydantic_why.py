from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    age: int = Field(gt=0, lt=200)
    weight: float
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    email: EmailStr
    linkedin_url: Annotated[AnyUrl, Field(max_length=50, title="LinkedIn profile of the patient", description="Provide linkedIn profile of the patient", examples=["https://linkedin.com/1322"])]
    
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