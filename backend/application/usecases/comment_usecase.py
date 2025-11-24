from domain.errors import (
    CommentNotFoundError,
    PostNotFoundError,
    UnauthorizedError,
)
from infrastructure.data.models.comment_model import Comment
from infrastructure.repositories.comment_repo import CommentRepository
from infrastructure.repositories.post_repo import PostRepository
from infrastructure.websocket.manager import manager
from presentation.schemas.comment_schema import CommentCreate, CommentUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class CommentUsecase:
    def __init__(self, db: AsyncSession):
        self.comment_repo = CommentRepository(db)
        self.post_repo = PostRepository(db)

    async def create_comment(
        self,
        post_id: int,
        author_id: int,
        comment_data: CommentCreate,
    ) -> Comment:
        # Verify post exists
        post = await self.post_repo.get_post_by_id(post_id, include_author=False)
        if not post:
            raise PostNotFoundError

        # Check if parent comment exists (if provided)
        if comment_data.parent_comment_id:
            parent = await self.comment_repo.get_comment_by_id(
                comment_data.parent_comment_id, include_author=False
            )
            if not parent:
                raise CommentNotFoundError

        comment = await self.comment_repo.create_comment(
            post_id=post_id,
            author_id=author_id,
            content=comment_data.content,
            parent_comment_id=comment_data.parent_comment_id
            if comment_data.parent_comment_id
            else None,
        )

        # Increment post comments count
        await self.post_repo.increment_comments_count(post_id)

        # Emit WebSocket event
        if comment_data.parent_comment_id:
            await manager.broadcast_to_post(
                post_id,
                {
                    "type": "comment:replied",
                    "comment_id": comment.id,
                    "parent_comment_id": comment_data.parent_comment_id,
                    "post_id": post_id,
                    "author_id": author_id,
                },
            )
        else:
            await manager.broadcast_to_post(
                post_id,
                {
                    "type": "post:commented",
                    "comment_id": comment.id,
                    "post_id": post_id,
                    "author_id": author_id,
                },
            )

        return comment

    async def get_comment(self, comment_id: int) -> Comment:
        comment = await self.comment_repo.get_comment_by_id(comment_id)
        if not comment:
            raise CommentNotFoundError
        return comment

    async def get_comments_by_post(
        self,
        post_id: int,
        skip: int = 0,
        limit: int = 50,
        sort_by: str = "newest",
        top_level_only: bool = True,
    ) -> tuple[list[Comment], int]:
        # Verify post exists
        post = await self.post_repo.get_post_by_id(post_id, include_author=False)
        if not post:
            raise PostNotFoundError

        return await self.comment_repo.get_comments_by_post(
            post_id=post_id,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            top_level_only=top_level_only,
        )

    async def get_replies_by_comment(
        self,
        comment_id: int,
        skip: int = 0,
        limit: int = 50,
        sort_by: str = "newest",
    ) -> tuple[list[Comment], int]:
        # Verify comment exists
        comment = await self.comment_repo.get_comment_by_id(
            comment_id, include_author=False
        )
        if not comment:
            raise CommentNotFoundError

        return await self.comment_repo.get_replies_by_comment(
            comment_id=comment_id, skip=skip, limit=limit, sort_by=sort_by
        )

    async def update_comment(
        self, comment_id: int, user_id: int, comment_data: CommentUpdate
    ) -> Comment:
        comment = await self.comment_repo.get_comment_by_id(comment_id)
        if not comment:
            raise CommentNotFoundError

        if comment.author_id != user_id:
            raise UnauthorizedError

        updated_comment = await self.comment_repo.update_comment(
            comment_id=comment_id, content=comment_data.content
        )

        if not updated_comment:
            raise CommentNotFoundError

        return updated_comment

    async def delete_comment(self, comment_id: int, user_id: int) -> bool:
        comment = await self.comment_repo.get_comment_by_id(comment_id)
        if not comment:
            raise CommentNotFoundError

        if comment.author_id != user_id:
            raise UnauthorizedError

        # Decrement post comments count
        await self.post_repo.decrement_comments_count(comment.post_id)

        return await self.comment_repo.delete_comment(comment_id)
