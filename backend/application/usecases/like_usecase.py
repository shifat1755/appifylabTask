from domain.errors import CommentNotFoundError, PostNotFoundError
from infrastructure.data.models.like_model import Like, LikeTargetType
from infrastructure.data.redis_notification_service import NotificationService
from infrastructure.repositories.comment_repo import CommentRepository
from infrastructure.repositories.like_repo import LikeRepository
from infrastructure.repositories.post_repo import PostRepository
from infrastructure.repositories.user_repo import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class LikeUsecase:
    def __init__(self, db: AsyncSession):
        self.like_repo = LikeRepository(db)
        self.post_repo = PostRepository(db)
        self.comment_repo = CommentRepository(db)
        self.user_repo = UserRepository(db)
        self.notification_service = NotificationService()

    async def toggle_like(
        self, user_id: int, target_id: int, target_type: str
    ) -> tuple[bool, int]:
        """
        Toggle like on a post or comment.
        Returns: (is_liked, total_likes)
        """
        like_target_type = LikeTargetType(target_type.lower())

        # Verify target exists
        post_id = None
        target_author_id = None
        if like_target_type == LikeTargetType.POST:
            post = await self.post_repo.get_post_by_id(target_id, include_author=True)
            if not post:
                raise PostNotFoundError
            post_id = target_id
            target_author_id = post.author_id
        else:  # COMMENT
            comment = await self.comment_repo.get_comment_by_id(
                target_id, include_author=True
            )
            if not comment:
                raise CommentNotFoundError
            post_id = comment.post_id
            target_author_id = comment.author_id

        # Check if already liked
        existing_like = await self.like_repo.get_like(
            user_id, target_id, like_target_type
        )

        if existing_like:
            # Unlike
            await self.like_repo.delete_like(user_id, target_id, like_target_type)
            is_liked = False

            # Decrement count
            if like_target_type == LikeTargetType.POST:
                await self.post_repo.decrement_likes_count(target_id)
            else:
                await self.comment_repo.decrement_likes_count(target_id)
        else:
            # Like
            await self.like_repo.create_like(user_id, target_id, like_target_type)
            is_liked = True

            # Increment count
            if like_target_type == LikeTargetType.POST:
                await self.post_repo.increment_likes_count(target_id)
            else:
                await self.comment_repo.increment_likes_count(target_id)

            # Create notification (only if user is liking someone else's content)
            if target_author_id and target_author_id != user_id:
                actor = await self.user_repo.get_user_by_id(user_id)
                if actor:
                    actor_name = f"{actor.first_name} {actor.last_name}"
                    if like_target_type == LikeTargetType.POST:
                        await self.notification_service.create_notification(
                            user_id=target_author_id,
                            notification_type="post_liked",
                            message=f"{actor_name} liked your post",
                            post_id=post_id,
                            actor_id=user_id,
                        )
                    else:
                        await self.notification_service.create_notification(
                            user_id=target_author_id,
                            notification_type="comment_liked",
                            message=f"{actor_name} liked your comment",
                            post_id=post_id,
                            comment_id=target_id,
                            actor_id=user_id,
                        )

        # Get updated like count
        total_likes = await self.like_repo.get_like_count(target_id, like_target_type)

        return is_liked, total_likes

    async def get_likes(
        self, target_id: int, target_type: str, skip: int = 0, limit: int = 50
    ) -> tuple[list[Like], int]:
        like_target_type = LikeTargetType(target_type.lower())
        return await self.like_repo.get_likes_by_target(
            target_id, like_target_type, skip=skip, limit=limit
        )

    async def is_liked_by_user(
        self, user_id: int, target_id: int, target_type: str
    ) -> bool:
        like_target_type = LikeTargetType(target_type.lower())
        return await self.like_repo.is_liked_by_user(
            user_id, target_id, like_target_type
        )
