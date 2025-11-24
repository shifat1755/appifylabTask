import logging

from application.usecases.like_usecase import LikeUsecase
from domain.errors import CommentNotFoundError, PostNotFoundError
from fastapi import APIRouter, Depends, HTTPException, Query
from infrastructure.data.database import get_db
from presentation.routes.dependencies import get_current_user
from presentation.schemas.like_schema import (
    LikeList,
    LikeRead,
    LikeToggleResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession

likeRouter = APIRouter(tags=["Likes"])

logger = logging.getLogger(__name__)


@likeRouter.post("/posts/{post_id}/like", response_model=LikeToggleResponse)
async def toggle_post_like(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Toggle like on a post."""
    usecase = LikeUsecase(db)
    try:
        user_id = int(current_user["user_id"])
        is_liked, total_likes = await usecase.toggle_like(user_id, post_id, "post")
        return LikeToggleResponse(is_liked=is_liked, total_likes=total_likes)
    except PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception:
        logger.exception("Error toggling post like")
        raise HTTPException(status_code=500, detail="Internal server error")


@likeRouter.get("/posts/{post_id}/likes", response_model=LikeList)
async def get_post_likes(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get all users who liked a post."""
    usecase = LikeUsecase(db)
    try:
        likes, total = await usecase.get_likes(
            target_id=post_id, target_type="post", skip=skip, limit=limit
        )
        return LikeList(
            likes=[LikeRead.model_validate(like) for like in likes],
            total=total,
            skip=skip,
            limit=limit,
        )
    except Exception:
        logger.exception("Error fetching post likes")
        raise HTTPException(status_code=500, detail="Internal server error")


@likeRouter.post("/comments/{comment_id}/like", response_model=LikeToggleResponse)
async def toggle_comment_like(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Toggle like on a comment."""
    usecase = LikeUsecase(db)
    try:
        user_id = int(current_user["user_id"])
        target_type = "comment"
        is_liked, total_likes = await usecase.toggle_like(
            user_id, comment_id, target_type
        )
        return LikeToggleResponse(is_liked=is_liked, total_likes=total_likes)
    except CommentNotFoundError:
        raise HTTPException(status_code=404, detail="Comment not found")
    except Exception:
        logger.exception("Error toggling comment like")
        raise HTTPException(status_code=500, detail="Internal server error")


@likeRouter.get("/comments/{comment_id}/likes", response_model=LikeList)
async def get_comment_likes(
    comment_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get all users who liked a comment."""
    usecase = LikeUsecase(db)
    try:
        target_type = "comment"
        likes, total = await usecase.get_likes(
            target_id=comment_id, target_type=target_type, skip=skip, limit=limit
        )
        return LikeList(
            likes=[LikeRead.model_validate(like) for like in likes],
            total=total,
            skip=skip,
            limit=limit,
        )
    except CommentNotFoundError:
        raise HTTPException(status_code=404, detail="Comment not found")
    except Exception:
        logger.exception("Error fetching comment likes")
        raise HTTPException(status_code=500, detail="Internal server error")
