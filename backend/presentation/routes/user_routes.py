from application.usecases.user_usecase import UserUsecase
from domain.errors import UserNotFoundError
from fastapi import APIRouter, Depends, HTTPException
from infrastructure.data.database import get_db
from presentation.routes.dependencies import get_current_user
from presentation.schemas.user_schema import UserRead
from sqlalchemy.ext.asyncio import AsyncSession

# from pydantic import model_validator


userRouter = APIRouter(prefix="/users")


@userRouter.get("/me", response_model=UserRead)
async def userInfo(
    sender=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    usecase = UserUsecase(db)
    try:
        res = await usecase.getUser(int(sender["user_id"]))
        return UserRead.model_validate(res)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
