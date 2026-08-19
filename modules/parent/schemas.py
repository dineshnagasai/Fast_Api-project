from pydantic import BaseModel,EmailStr #basemodel gives the class a strict behavior
class ParentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    occupation: str
    address: str

class ParentResponse(BaseModel):
    id: int

    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    occupation: str
    address: str

    model_config = {
        "from_attributes": True
    }
