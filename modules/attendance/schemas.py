from datetime import time
from pydantic import BaseModel

class StudentAttendanceCreate(BaseModel):
    date: str
    status: str
    check_in: time
    check_out: time
    remarks: str
    student_id: int

class StudentAttendanceResponse(BaseModel):
    id: int
    date: str
    status: str
    check_in: time
    check_out: time
    remarks: str
    student_id: int

    model_config = {
        "from_attributes": True
    }
class TeacherAttendanceCreate(BaseModel):
    date: str
    status: str
    check_in: time
    check_out: time
    remarks: str
    teacher_id: int

class TeacherAttendanceResponse(BaseModel):
    id: int
    date: str
    status: str
    check_in: time
    check_out: time
    remarks: str
    teacher_id: int

    model_config = {
        "from_attributes": True
    }


