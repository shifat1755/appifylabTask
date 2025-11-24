import logging
from typing import Optional

from application.usecases.post_usecase import PostUsecase
from domain.errors import (
    PostAccessDeniedError,
    PostNotFoundError,
    UnauthorizedError,
)
from fastapi import APIRouter, Depends, HTTPException, Query
from infrastructure.data.database import get_db
from presentation.routes.dependencies import get_current_user, get_current_user_optional
from presentation.schemas.post_schema import (
    PostCreate,
    PostList,
    PostRead,
    PostUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession

postRouter = APIRouter(prefix="/posts", tags=["Posts"])

logger = logging.getLogger(__name__)


@postRouter.post("", response_model=PostRead, status_code=201)
async def create_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new post."""
    usecase = PostUsecase(db)
    try:
        user_id = int(current_user["user_id"])
        post = await usecase.create_post(author_id=user_id, post_data=post_data)
        return PostRead.model_validate(post)
    except UnauthorizedError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception:
        logger.exception("Error creating post")
        raise HTTPException(status_code=500, detail="Internal server error")


@postRouter.get("", response_model=PostList)
async def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    author_id: Optional[int] = Query(None),
    visibility: Optional[str] = Query(None, regex="^(public|private)$"),
    sort_by: str = Query("newest", regex="^(newest|oldest|most_liked|most_commented)$"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """Get all posts with pagination and filters."""
    usecase = PostUsecase(db)
    try:
        current_user_id = int(current_user["user_id"]) if current_user else None
        posts, total = await usecase.get_posts(
            skip=skip,
            limit=limit,
            author_id=author_id,
            visibility=visibility,
            current_user_id=current_user_id,
            sort_by=sort_by,
        )
        return PostList(
            posts=[PostRead.model_validate(post) for post in posts],
            total=total,
            skip=skip,
            limit=limit,
        )
    except Exception:
        logger.exception("Error fetching posts")
        raise HTTPException(status_code=500, detail="Internal server error")


@postRouter.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """Get a single post by ID."""
    usecase = PostUsecase(db)
    try:
        current_user_id = int(current_user["user_id"]) if current_user else None
        post = await usecase.get_post(post_id, current_user_id=current_user_id)
        return PostRead.model_validate(post)
    except PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")
    except PostAccessDeniedError:
        raise HTTPException(status_code=403, detail="Access denied to private post")
    except Exception:
        logger.exception("Error fetching post")
        raise HTTPException(status_code=500, detail="Internal server error")


@postRouter.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update a post (only by author)."""
    usecase = PostUsecase(db)
    try:
        user_id = int(current_user["user_id"])
        post = await usecase.update_post(post_id, user_id, post_data)
        return PostRead.model_validate(post)
    except PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")
    except UnauthorizedError:
        raise HTTPException(
            status_code=403, detail="Only the author can update this post"
        )
    except Exception:
        logger.exception("Error updating post")
        raise HTTPException(status_code=500, detail="Internal server error")


@postRouter.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a post (only by author)."""
    usecase = PostUsecase(db)
    try:
        user_id = int(current_user["user_id"])
        deleted = await usecase.delete_post(post_id, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Post not found")
        return None
    except PostNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")
    except UnauthorizedError:
        raise HTTPException(
            status_code=403, detail="Only the author can delete this post"
        )
    except Exception:
        logger.exception("Error deleting post")
        raise HTTPException(status_code=500, detail="Internal server error")
