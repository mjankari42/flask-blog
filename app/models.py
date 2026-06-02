from datetime import UTC, datetime
from hashlib import md5

from flask_login import UserMixin
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, WriteOnlyMapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):  # ty: ignore
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(256))
    posts: WriteOnlyMapped[Post] = relationship(back_populates="author")

    def __repr__(self):
        return f"User {self.username}"

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:

        if self.password_hash is None:
            return False

        return check_password_hash(self.password_hash, password)

    def avatar(self, size: int):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


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


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
