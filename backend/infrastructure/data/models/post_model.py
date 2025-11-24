from datetime import datetime
from enum import Enum

from infrastructure.data.database import Base
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy import (
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class PostVisibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    visibility: Mapped[PostVisibility] = mapped_column(
        SQLEnum(PostVisibility, values_callable=lambda x: [m.value for m in x]),
        default=PostVisibility.PUBLIC,
        nullable=False,
    )
    likes_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comments_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="posts")  # noqa: F821
    comments: Mapped[list["Comment"]] = relationship(  # noqa: F821
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
