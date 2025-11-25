from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class NotificationRead(BaseModel):
    id: str
    user_id: int
    type: str
    message: str
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    actor_id: Optional[int] = None
    created_at: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "1:1234567890.123",
                "user_id": 1,
                "type": "post_liked",
                "message": "John Doe liked your post",
                "post_id": 5,
                "actor_id": 2,
                "created_at": "2025-01-27T12:00:00",
            }
        }
    )


class NotificationList(BaseModel):
    notifications: List[NotificationRead]
    unread_count: int  # This is just the count of notifications returned

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notifications": [],
                "unread_count": 0,
            }
        }
    )
