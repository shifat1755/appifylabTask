from typing import Optional
from typing import list as ListType

from infrastructure.data.models.like_model import Like, LikeTargetType
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class LikeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_like(
        self, user_id: int, target_id: int, target_type: LikeTargetType
    ) -> Like:
        db_like = Like(user_id=user_id, target_id=target_id, target_type=target_type)
        try:
            self.db.add(db_like)
            await self.db.commit()
            await self.db.refresh(db_like)
            return db_like
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_like(
        self, user_id: int, target_id: int, target_type: LikeTargetType
    ) -> Optional[Like]:
        stmt = select(Like).where(
            and_(
                Like.user_id == user_id,
                Like.target_id == target_id,
                Like.target_type == target_type,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def delete_like(
        self, user_id: int, target_id: int, target_type: LikeTargetType
    ) -> bool:
        stmt = select(Like).where(
            and_(
                Like.user_id == user_id,
                Like.target_id == target_id,
                Like.target_type == target_type,
            )
        )
        result = await self.db.execute(stmt)
        like = result.scalars().first()

        if not like:
            return False

        try:
            await self.db.delete(like)
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_likes_by_target(
        self,
        target_id: int,
        target_type: LikeTargetType,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[ListType[Like], int]:
        stmt = select(Like).where(
            and_(Like.target_id == target_id, Like.target_type == target_type)
        )
        count_stmt = (
            select(func.count())
            .select_from(Like)
            .where(and_(Like.target_id == target_id, Like.target_type == target_type))
        )

        stmt = stmt.options(selectinload(Like.user))
        stmt = stmt.offset(skip).limit(limit)

        result = await self.db.execute(stmt)
        likes = result.scalars().all()

        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0

        return likes, total

    async def get_like_count(self, target_id: int, target_type: LikeTargetType) -> int:
        stmt = (
            select(func.count())
            .select_from(Like)
            .where(and_(Like.target_id == target_id, Like.target_type == target_type))
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0

    async def is_liked_by_user(
        self, user_id: int, target_id: int, target_type: LikeTargetType
    ) -> bool:
        like = await self.get_like(user_id, target_id, target_type)
        return like is not None
