from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class LikeTargetTypeEnum(str, Enum):
    POST = "post"
    COMMENT = "comment"


# --------------------------
# Output / Response schemas
# --------------------------
class UserInfo(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class LikeRead(BaseModel):
    id: int
    user_id: int
    target_id: int
    target_type: LikeTargetTypeEnum
    created_at: datetime
    user: Optional[UserInfo] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "target_id": 1,
                "target_type": "post",
                "created_at": "2025-01-27T12:00:00Z",
            }
        },
    )


class LikeList(BaseModel):
    likes: List[LikeRead]
    total: int
    skip: int
    limit: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "likes": [],
                "total": 0,
                "skip": 0,
                "limit": 50,
            }
        }
    )


class LikeToggleResponse(BaseModel):
    is_liked: bool
    total_likes: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "is_liked": True,
                "total_likes": 5,
            }
        }
    )
