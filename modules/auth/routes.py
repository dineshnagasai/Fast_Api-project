from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.database import get_db
from modules.auth.schemas import LoginRequest
from modules.auth.services import login
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login_api(login_data: OAuth2PasswordRequestForm = Depends(),db: AsyncSession = Depends(get_db)):
    return await login(login_data, db)