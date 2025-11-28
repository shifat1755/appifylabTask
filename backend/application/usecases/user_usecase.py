from domain.errors import UserNotFoundError
from infrastructure.data.models.user_model import User
from infrastructure.repositories.user_repo import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserUsecase:
    def __init__(self, db: AsyncSession):
        self.userRepo = UserRepository(db)

    async def getUser(self, user_id: int) -> User:
        user = await self.userRepo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError
        return user
