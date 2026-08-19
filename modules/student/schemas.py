from pydantic import BaseModel,EmailStr #basemodel gives the class a strict behavior

class StudentResponse(BaseModel):  # StudentResponse does not create student.creates a blueprint for a valid model(schema)
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    age: int
    department: str
    parents:list[str]
    teacher_ids: list[int]

    model_config = {
        "from_attributes": True
    }
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

    age: int
    department: str

    model_config = {
        "from_attributes": True
    }
