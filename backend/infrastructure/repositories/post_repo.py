from typing import Optional
from datetime import datetime, timezone

from infrastructure.data.models.post_model import Post, PostVisibility
from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_post(
        self,
        author_id: int,
        content: str,
        image_url: Optional[str] = None,
        visibility: PostVisibility = PostVisibility.PUBLIC,
    ) -> Post:
        db_post = Post(
            author_id=author_id,
            content=content,
            image_url=image_url,
            visibility=visibility,
        )
        try:
            self.db.add(db_post)
            await self.db.commit()
            await self.db.refresh(db_post)
            return db_post
        except Exception as e:
            await self.db.rollback()
            raise e

    async def get_post_by_id(
        self, post_id: int, include_author: bool = True
    ) -> Optional[Post]:
        stmt = select(Post).where(Post.id == post_id)
        if include_author:
            stmt = stmt.options(selectinload(Post.author))
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_posts(
        self,
        skip: int = 0,
        limit: int = 20,
        author_id: Optional[int] = None,
        visibility: Optional[PostVisibility] = None,
        current_user_id: Optional[int] = None,
        sort_by: str = "newest",
    ) -> tuple[list[Post], int]:
        # Base query
        stmt = select(Post)
        count_stmt = select(func.count()).select_from(Post)

        # Apply filters
        conditions = []
        if author_id:
            conditions.append(Post.author_id == author_id)
        if visibility:
            conditions.append(Post.visibility == visibility)
        elif current_user_id is not None:
            # Show public posts or private posts owned by current user
            conditions.append(
                (Post.visibility == PostVisibility.PUBLIC)
                | ((Post.visibility == PostVisibility.PRIVATE) & (Post.author_id == current_user_id))
            )
        else:
            # If no user, only show public posts
            conditions.append(Post.visibility == PostVisibility.PUBLIC)

        if conditions:
            stmt = stmt.where(*conditions)
            count_stmt = count_stmt.where(*conditions)

        # Apply sorting
        if sort_by == "newest":
            stmt = stmt.order_by(desc(Post.created_at))
        elif sort_by == "oldest":
            stmt = stmt.order_by(asc(Post.created_at))
        elif sort_by == "most_liked":
            stmt = stmt.order_by(desc(Post.likes_count))
        elif sort_by == "most_commented":
            stmt = stmt.order_by(desc(Post.comments_count))

        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        stmt = stmt.options(selectinload(Post.author))

        # Execute queries
        result = await self.db.execute(stmt)
        posts = result.scalars().all()

        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0

        return posts, total

    async def update_post(
        self,
        post_id: int,
        content: Optional[str] = None,
        image_url: Optional[str] = None,
        visibility: Optional[PostVisibility] = None,
    ) -> Optional[Post]:
        stmt = select(Post).where(Post.id == post_id)
        result = await self.db.execute(stmt)
        post = result.scalars().first()

        if not post:
            return None

        if content is not None:
            post.content = content
        if image_url is not None:
            post.image_url = image_url
        if visibility is not None:
            post.visibility = visibility

        post.updated_at = datetime.now(timezone.utc)

        try:
            await self.db.commit()
            await self.db.refresh(post)
            return post
        except Exception as e:
            await self.db.rollback()
            raise e

    async def delete_post(self, post_id: int) -> bool:
        stmt = select(Post).where(Post.id == post_id)
        result = await self.db.execute(stmt)
        post = result.scalars().first()

        if not post:
            return False

        try:
            await self.db.delete(post)
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            raise e

    async def increment_likes_count(self, post_id: int) -> None:
        stmt = select(Post).where(Post.id == post_id)
        result = await self.db.execute(stmt)
        post = result.scalars().first()
        if post:
            post.likes_count += 1
            await self.db.commit()

    async def decrement_likes_count(self, post_id: int) -> None:
        stmt = select(Post).where(Post.id == post_id)
        result = await self.db.execute(stmt)
        post = result.scalars().first()
        if post:
            post.likes_count = max(0, post.likes_count - 1)
            await self.db.commit()

    async def increment_comments_count(self, post_id: int) -> None:
        stmt = select(Post).where(Post.id == post_id)
        result = await self.db.execute(stmt)
        post = result.scalars().first()
        if post:
            post.comments_count += 1
            await self.db.commit()

    async def decrement_comments_count(self, post_id: int) -> None:
        stmt = select(Post).where(Post.id == post_id)
        result = await self.db.execute(stmt)
        post = result.scalars().first()
        if post:
            post.comments_count = max(0, post.comments_count - 1)
            await self.db.commit()

