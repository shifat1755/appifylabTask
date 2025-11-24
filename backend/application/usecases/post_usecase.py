from typing import Optional

from domain.errors import PostAccessDeniedError, PostNotFoundError, UnauthorizedError
from infrastructure.data.models.post_model import Post, PostVisibility
from infrastructure.repositories.post_repo import PostRepository
from infrastructure.repositories.user_repo import UserRepository
from presentation.schemas.post_schema import PostCreate, PostUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class PostUsecase:
    def __init__(self, db: AsyncSession):
        self.post_repo = PostRepository(db)
        self.user_repo = UserRepository(db)

    async def create_post(self, author_id: int, post_data: PostCreate) -> Post:
        # Verify user exists
        user = await self.user_repo.get_user_by_id(author_id)
        if not user:
            raise UnauthorizedError
        post = await self.post_repo.create_post(
            author_id=author_id,
            content=post_data.content,
            image_url=post_data.image_url,
            visibility=PostVisibility(post_data.visibility)
            if post_data.visibility
            else PostVisibility.PUBLIC,
        )
        post.author = user
        return post

    async def get_post(
        self, post_id: int, current_user_id: Optional[int] = None
    ) -> Post:
        post = await self.post_repo.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError

        # Check visibility
        if post.visibility == PostVisibility.PRIVATE:
            if not current_user_id or post.author_id != current_user_id:
                raise PostAccessDeniedError

        return post

    async def get_posts(
        self,
        skip: int = 0,
        limit: int = 20,
        author_id: Optional[int] = None,
        visibility: Optional[str] = None,
        current_user_id: Optional[int] = None,
        sort_by: str = "newest",
    ) -> tuple[list[Post], int]:
        post_visibility = PostVisibility(visibility) if visibility else None
        return await self.post_repo.get_posts(
            skip=skip,
            limit=limit,
            author_id=author_id,
            visibility=post_visibility,
            current_user_id=current_user_id,
            sort_by=sort_by,
        )

    async def update_post(
        self, post_id: int, user_id: int, post_data: PostUpdate
    ) -> Post:
        post = await self.post_repo.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError

        if post.author_id != user_id:
            raise UnauthorizedError

        visibility = (
            PostVisibility(post_data.visibility) if post_data.visibility else None
        )

        updated_post = await self.post_repo.update_post(
            post_id=post_id,
            content=post_data.content,
            image_url=post_data.image_url,
            visibility=visibility,
        )

        if not updated_post:
            raise PostNotFoundError

        return updated_post

    async def delete_post(self, post_id: int, user_id: int) -> bool:
        post = await self.post_repo.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError

        if post.author_id != user_id:
            raise UnauthorizedError

        return await self.post_repo.delete_post(post_id)
