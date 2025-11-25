import logging

from fastapi import APIRouter, Depends, HTTPException
from infrastructure.data.redis_notification_service import NotificationService
from presentation.routes.dependencies import get_current_user
from presentation.schemas.notification_schema import NotificationList

notificationRouter = APIRouter(prefix="/notifications", tags=["Notifications"])

logger = logging.getLogger(__name__)


@notificationRouter.get("", response_model=NotificationList)
async def get_notifications(
    current_user: dict = Depends(get_current_user),
):
    """Get notifications for the current user and delete them from Redis."""
    try:
        user_id = int(current_user["user_id"])
        notification_service = NotificationService()
        
        notifications = await notification_service.get_and_delete_notifications(
            user_id=user_id
        )
        
        return NotificationList(
            notifications=notifications,
            unread_count=len(notifications),
        )
    except Exception:
        logger.exception("Error fetching notifications")
        raise HTTPException(status_code=500, detail="Internal server error")
