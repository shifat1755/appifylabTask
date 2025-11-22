from typing import Optional

from infrastructure.data.models.user_model import User
from presentation.schemas.user_schema import UserCreate
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # Create user
    async def create_user(self, user: UserCreate, hashed_password: str) -> User:
        db_user = User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            bio=user.bio,
            avatar_url=user.avatar_url,
            hashed_password=hashed_password,
        )

        try:
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except Exception as e:
            self.db.rollback()
            raise e

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        res = await self.db.execute(stmt)
        return res.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()
