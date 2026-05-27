from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    age: int 
    weight: float #kg
    height: float #m
    allergies: List[str]
    email: EmailStr
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    
    
patient_info = {
    "name": "Nitish",  
    "age": 30,
    "weight": 60,
    "height": 1.6,
    "allergies": ["pollen", "dust"],
    "email": "abc@gmail.com",
    }
patient1= Patient(**patient_info)

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.bmi)

insert_patient(patient1)