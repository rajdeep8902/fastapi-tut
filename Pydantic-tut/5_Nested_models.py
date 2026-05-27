from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    gender: str
    age: int
    address: Address
    
address_dict = {
    "city": "Thakurnagar",
    "state": "West Bengal",
    "pin": "743287"
}
address1 = Address(**address_dict)

patient_dict = {
    "name": "Rajdeep",
    "gender": "male",
    "age": 35,
    "address": address1
}
patient1= Patient(**patient_dict)

print(patient1)