from datetime import datetime
from enum import Enum

from infrastructure.data.database import Base
from sqlalchemy import DateTime, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class LikeTargetType(str, Enum):
    POST = "post"
    COMMENT = "comment"


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)

    target_type: Mapped[LikeTargetType] = mapped_column(
        SQLEnum(
            LikeTargetType,
            values_callable=lambda x: [m.value for m in x],
        ),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="likes")  # noqa: F821

    __table_args__ = (
        UniqueConstraint(
            "user_id", "target_id", "target_type", name="unique_user_like"
        ),
        Index(
            "ix_like_target_and_type", "target_type", "target_id"
        ),  # composite index for faster lookups
    )
