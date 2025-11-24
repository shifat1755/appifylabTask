import logging

from application.usecases.comment_usecase import CommentUsecase
from domain.errors import CommentNotFoundError, PostNotFoundError, UnauthorizedError
from fastapi import APIRouter, Depends, HTTPException, Query
from infrastructure.data.database import get_db
from presentation.routes.dependencies import get_current_user
from presentation.schemas.comment_schema import (
    CommentCreate,
    CommentList,
    CommentRead,
    CommentUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession

commentRouter = APIRouter(tags=["Comments"])

logger = logging.getLogger(__name__)


@commentRouter.post(
    "/posts/{post_id}/comments", response_model=CommentRead, status_code=201
)
async def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a comment on a post."""
    usecase = CommentUsecase(db)
    try:
        user_id = int(current_user["user_id"])
        print("Whats_wrong!")
        comment = await usecase.create_comment(
            post_id=post_id, author_id=user_id, comment_data=comment_data
        )
        return CommentRead.model_validate(comment)
    except PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")
    except CommentNotFoundError:
        raise HTTPException(status_code=404, detail="Parent comment not found")
    except Exception:
        logger.exception("Error creating comment")
        raise HTTPException(status_code=500, detail="Internal server error")


@commentRouter.get("/posts/{post_id}/comments", response_model=CommentList)
async def get_comments_by_post(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    sort_by: str = Query("newest", regex="^(newest|oldest|most_liked)$"),
    top_level_only: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    sender_id: int = Depends(get_current_user),
):
    """Get all comments for a post."""
    usecase = CommentUsecase(db)
    try:
        comments, total = await usecase.get_comments_by_post(
            post_id=post_id,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            top_level_only=top_level_only,
        )
        return CommentList(
            comments=[CommentRead.model_validate(comment) for comment in comments],
            total=total,
            skip=skip,
            limit=limit,
        )
    except PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")
    except Exception:
        logger.exception("Error fetching comments")
        raise HTTPException(status_code=500, detail="Internal server error")


@commentRouter.get("/comments/{comment_id}/replies", response_model=CommentList)
async def get_replies_by_comment(
    comment_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    sort_by: str = Query("newest", regex="^(newest|oldest|most_liked)$"),
    db: AsyncSession = Depends(get_db),
    sender_id: int = Depends(get_current_user),
):
    """Get all replies for a comment."""
    usecase = CommentUsecase(db)
    try:
        replies, total = await usecase.get_replies_by_comment(
            comment_id=comment_id, skip=skip, limit=limit, sort_by=sort_by
        )
        return CommentList(
            comments=[CommentRead.model_validate(reply) for reply in replies],
            total=total,
            skip=skip,
            limit=limit,
        )
    except CommentNotFoundError:
        raise HTTPException(status_code=404, detail="Comment not found")
    except Exception:
        logger.exception("Error fetching replies")
        raise HTTPException(status_code=500, detail="Internal server error")


@commentRouter.put("/comment/{comment_id}", response_model=CommentRead)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update a comment (only by author)."""
    usecase = CommentUsecase(db)
    try:
        user_id = int(current_user["user_id"])
        comment = await usecase.update_comment(comment_id, user_id, comment_data)
        return CommentRead.model_validate(comment)
    except CommentNotFoundError:
        raise HTTPException(status_code=404, detail="Comment not found")
    except UnauthorizedError:
        raise HTTPException(
            status_code=403, detail="Only the author can update this comment"
        )
    except Exception:
        logger.exception("Error updating comment")
        raise HTTPException(status_code=500, detail="Internal server error")


@commentRouter.delete("/comment/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a comment (only by author)."""
    usecase = CommentUsecase(db)
    try:
        user_id = int(current_user["user_id"])
        deleted = await usecase.delete_comment(comment_id, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Comment not found")
        return None
    except CommentNotFoundError:
        raise HTTPException(status_code=404, detail="Comment not found")
    except UnauthorizedError:
        raise HTTPException(
            status_code=403, detail="Only the author can delete this comment"
        )
    except Exception:
        logger.exception("Error deleting comment")
        raise HTTPException(status_code=500, detail="Internal server error")
