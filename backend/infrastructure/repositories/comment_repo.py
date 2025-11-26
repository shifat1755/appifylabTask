from datetime import datetime, timezone
from typing import Optional

from infrastructure.data.models.comment_model import Comment
from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_comment(
        self,
        post_id: int,
        author_id: int,
        content: str,
        parent_comment_id: Optional[int] = None,
    ) -> Comment:
        print("inside_comment_repo")
        db_comment = Comment(
            post_id=post_id,
            author_id=author_id,
            content=content,
            parent_comment_id=parent_comment_id,
        )
        try:
            self.db.add(db_comment)
            await self.db.commit()
            await self.db.refresh(db_comment)
            # eager load
            res = await self.db.execute(
                select(Comment)
                .options(selectinload(Comment.author))
                .where(Comment.id == db_comment.id)
            )
            db_comment = res.scalars().first()
            return db_comment
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_comment_by_id(
        self, comment_id: int, include_author: bool = False
    ) -> Optional[Comment]:
        stmt = select(Comment).where(Comment.id == comment_id)
        if include_author:
            stmt = stmt.options(selectinload(Comment.author))
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_comments_by_post(
        self,
        post_id: int,
        skip: int = 0,
        limit: int = 50,
        sort_by: str = "newest",
        top_level_only: bool = True,
    ) -> tuple[list[Comment], int]:
        stmt = select(Comment).where(Comment.post_id == post_id)
        count_stmt = (
            select(func.count()).select_from(Comment).where(Comment.post_id == post_id)
        )

        if top_level_only:
            stmt = stmt.where(Comment.parent_comment_id.is_(None))
            count_stmt = count_stmt.where(Comment.parent_comment_id.is_(None))

        # Apply sorting
        if sort_by == "newest":
            stmt = stmt.order_by(desc(Comment.created_at))
        elif sort_by == "oldest":
            stmt = stmt.order_by(asc(Comment.created_at))
        elif sort_by == "most_liked":
            stmt = stmt.order_by(desc(Comment.likes_count))

        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        stmt = stmt.options(selectinload(Comment.author))

        result = await self.db.execute(stmt)
        comments = result.scalars().all()

        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0

        return comments, total

    async def get_replies_by_comment(
        self,
        comment_id: int,
        skip: int = 0,
        limit: int = 50,
        sort_by: str = "newest",
    ) -> tuple[list[Comment], int]:
        stmt = select(Comment).where(Comment.parent_comment_id == comment_id)
        count_stmt = (
            select(func.count())
            .select_from(Comment)
            .where(Comment.parent_comment_id == comment_id)
        )

        # Apply sorting
        if sort_by == "newest":
            stmt = stmt.order_by(desc(Comment.created_at))
        elif sort_by == "oldest":
            stmt = stmt.order_by(asc(Comment.created_at))
        elif sort_by == "most_liked":
            stmt = stmt.order_by(desc(Comment.likes_count))

        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        stmt = stmt.options(selectinload(Comment.author))

        result = await self.db.execute(stmt)
        replies = result.scalars().all()

        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0

        return replies, total

    async def update_comment(self, comment_id: int, content: str) -> Optional[Comment]:
        stmt = select(Comment).where(Comment.id == comment_id)
        result = await self.db.execute(stmt)
        comment = result.scalars().first()

        if not comment:
            return None

        comment.content = content
        comment.updated_at = datetime.now(timezone.utc)

        try:
            await self.db.commit()
            await self.db.refresh(comment)
            return comment
        except Exception as e:
            await self.db.rollback()
            raise e

    async def delete_comment(self, comment_id: int) -> bool:
        stmt = select(Comment).where(Comment.id == comment_id)
        result = await self.db.execute(stmt)
        comment = result.scalars().first()

        if not comment:
            return False

        try:
            await self.db.delete(comment)
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            raise e

    async def increment_likes_count(self, comment_id: int) -> None:
        stmt = select(Comment).where(Comment.id == comment_id)
        result = await self.db.execute(stmt)
        comment = result.scalars().first()
        if comment:
            comment.likes_count += 1
            await self.db.commit()

    async def decrement_likes_count(self, comment_id: int) -> None:
        stmt = select(Comment).where(Comment.id == comment_id)
        result = await self.db.execute(stmt)
        comment = result.scalars().first()
        if comment:
            comment.likes_count = max(0, comment.likes_count - 1)
            await self.db.commit()

    async def get_comment_count_by_post(self, post_id: int) -> int:
        stmt = (
            select(func.count()).select_from(Comment).where(Comment.post_id == post_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0
