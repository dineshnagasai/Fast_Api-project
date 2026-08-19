from sqlalchemy.ext.asyncio import AsyncSession
from modules.auth.schemas import LoginRequest
from sqlalchemy import select
from fastapi import HTTPException

from modules.user.models import User
from common.security import create_access_token

async def login(login_data: LoginRequest,db: AsyncSession):
    result = await db.execute(
        select(User).where(User.email == login_data.username)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if user.password != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }