from datetime import time
from pydantic import BaseModel,EmailStr

class AdminCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    designation: str

class AdminResponse(BaseModel):
    id: int

    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    designation: str

    model_config = {
        "from_attributes": True
    }