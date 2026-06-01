from datetime import UTC, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, WriteOnlyMapped, mapped_column, relationship

from app import db


class User(db.Model):  # ty: ignore
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(256))
    posts: WriteOnlyMapped[Post] = relationship(back_populates="author")

    def __repr__(self):
        return f"User {self.username}"


class Post(db.Model):  # ty: ignore
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String(140))
    timestamp: Mapped[datetime] = mapped_column(
        index=True, default=lambda: datetime.now(UTC)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True)
    author: Mapped[User] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"Post {self.body}"
