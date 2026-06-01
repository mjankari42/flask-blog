from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(256))

    def __repr__(self):
        return f"User {self.username}"
