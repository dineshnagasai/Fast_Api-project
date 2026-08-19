from pydantic import BaseModel,EmailStr

class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    subject: str
    qualification: str

class TeacherResponse(BaseModel):
    id: int

    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    subject: str
    qualification: str

    model_config = {
        "from_attributes": True
    }