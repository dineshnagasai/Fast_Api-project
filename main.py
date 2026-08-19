from fastapi import FastAPI
from modules.student import routes
from modules.parent.routes import router as parent_router
from modules.teacher.routes import router as teacher_router
from modules.attendance.routes import router as attendance_router
from modules.admin.routes import router as admin_router
from modules.auth.routes import router as auth_router
from fastapi import HTTPException
from common.exception import http_exception_handler
from modules.student.models import *
from modules.teacher.models import *
from modules.attendance.models import *
from modules.parent.models import *
from fastapi.exceptions import RequestValidationError
from common.exception import validation_exception_handler
from common.exception import global_exception_handler

app = FastAPI()
app.add_exception_handler(HTTPException,http_exception_handler)
app.add_exception_handler(RequestValidationError,validation_exception_handler)
app.add_exception_handler(Exception,global_exception_handler)
app.include_router(routes.router)
app.include_router(parent_router)
app.include_router(teacher_router)
app.include_router(attendance_router)
app.include_router(admin_router)
app.include_router(auth_router)