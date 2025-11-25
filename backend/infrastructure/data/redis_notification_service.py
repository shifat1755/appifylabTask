import json
from datetime import datetime
from typing import List, Optional

from config import RedisConfig
from redis.asyncio import Redis


class NotificationService:
    def __init__(self, redis_url: str | None = None):
        # Use a different Redis DB for notifications (e.g., DB 2)
        redis_url = (
            redis_url or f"redis://{RedisConfig.REDIS_HOST}:{RedisConfig.REDIS_PORT}/2"
        )
        self.redis: Redis = Redis.from_url(redis_url, decode_responses=True)

    async def create_notification(
        self,
        user_id: int,
        notification_type: str,
        message: str,
        post_id: Optional[int] = None,
        comment_id: Optional[int] = None,
        actor_id: Optional[int] = None,
    ) -> None:
        """Create a notification and store it in Redis."""
        notification = {
            "id": f"{user_id}:{datetime.now().timestamp()}",
            "user_id": user_id,
            "type": notification_type,  # "post_liked", "post_commented", "comment_liked"
            "message": message,
            "post_id": post_id,
            "comment_id": comment_id,
            "actor_id": actor_id,
            "created_at": datetime.now().isoformat(),
        }

        # Store in a list for the user
        key = f"notifications:{user_id}"
        await self.redis.lpush(key, json.dumps(notification))

        # Set expiration (7 days)
        await self.redis.expire(key, 7 * 24 * 60 * 60)

    async def get_and_delete_notifications(self, user_id: int) -> List[dict]:
        """Get all notifications for a user and delete them from Redis."""
        key = f"notifications:{user_id}"

        # Get all notifications
        notifications_data = await self.redis.lrange(key, 0, -1)

        notifications = []
        for notif_str in notifications_data:
            try:
                notif = json.loads(notif_str)
                notifications.append(notif)
            except json.JSONDecodeError:
                continue

        # Delete all notifications for this user
        if notifications_data:
            await self.redis.delete(key)

        return notifications
