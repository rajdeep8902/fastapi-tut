from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    allergies: List[str]
    email: EmailStr
    
    @field_validator("email")
    @classmethod
    def email_validator(cls, val):
        valid_domain = ["hdfc.com", "icici.com"]
        domain_name = val.split('@')[-1]
        if domain_name not in valid_domain:
            raise ValueError("Not a valid domain")
        return val
    
    @field_validator("name")
    @classmethod
    def transform_name(cls, val):
        return val.capitalize()
        
   
patient_info = {
    "name": "nitish",  
    "age": 30,
    "weight": 75.2,
    "allergies": ["pollen", "dust"],
    "email": "abc@icici.com"
    }
patient1= Patient(**patient_info)

def insert_patient(patient: Patient):
    print(patient1.name)
    print(patient1.age)
    print(patient1.email)

insert_patient(patient1)