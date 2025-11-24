from datetime import datetime
from typing import Optional, List
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class PostVisibilityEnum(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


# --------------------------
# Base schemas
# --------------------------
class PostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    image_url: Optional[str] = None
    visibility: Optional[PostVisibilityEnum] = PostVisibilityEnum.PUBLIC

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "content": "This is a sample post content.",
                "image_url": "https://example.com/image.jpg",
                "visibility": "public",
            }
        },
    )


# --------------------------
# Input schemas
# --------------------------
class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=10000)
    image_url: Optional[str] = None
    visibility: Optional[PostVisibilityEnum] = None

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "content": "Updated post content.",
                "image_url": "https://example.com/new-image.jpg",
                "visibility": "private",
            }
        },
    )


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


class PostRead(PostBase):
    id: int
    author_id: int
    likes_count: int
    comments_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[AuthorInfo] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "author_id": 1,
                "content": "This is a sample post content.",
                "image_url": "https://example.com/image.jpg",
                "visibility": "public",
                "likes_count": 5,
                "comments_count": 3,
                "created_at": "2025-01-27T12:00:00Z",
                "updated_at": "2025-01-27T13:00:00Z",
            }
        },
    )


class PostList(BaseModel):
    posts: List[PostRead]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "posts": [],
                "total": 0,
                "skip": 0,
                "limit": 20,
            }
        }
    )

