from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field


# --------------------------
# Base schemas
# --------------------------
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "content": "This is a sample comment.",
            }
        },
    )


# --------------------------
# Input schemas
# --------------------------
class CommentCreate(CommentBase):
    parent_comment_id: Optional[int] = None

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "content": "This is a sample comment.",
                "parent_comment_id": None,
            }
        },
    )


class CommentUpdate(CommentBase):
    pass


# --------------------------
# Output / Response schemas
# --------------------------
class AuthorInfo(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CommentRead(CommentBase):
    id: int
    post_id: int
    parent_comment_id: Optional[int] = None
    author_id: int
    likes_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[AuthorInfo] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "post_id": 1,
                "parent_comment_id": None,
                "author_id": 1,
                "content": "This is a sample comment.",
                "likes_count": 2,
                "created_at": "2025-01-27T12:00:00Z",
                "updated_at": None,
            }
        },
    )


class CommentList(BaseModel):
    comments: List[CommentRead]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "comments": [],
                "total": 0,
                "skip": 0,
                "limit": 50,
            }
        }
    )

