from datetime import UTC, datetime
from hashlib import md5

from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String, Table, func, or_, select
from sqlalchemy.orm import Mapped, WriteOnlyMapped, aliased, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from flask_blog import db, login

followers = Table(
    "followers",
    db.metadata,
    Column("follower_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("user.id"), primary_key=True),
)


class User(UserMixin, db.Model):  # ty: ignore
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(256))
    posts: WriteOnlyMapped[Post] = relationship(back_populates="author")
    about_me: Mapped[str | None] = mapped_column(String(140))
    last_seen: Mapped[datetime | None] = mapped_column(
        default=lambda: datetime.now(UTC)
    )
    following: WriteOnlyMapped[User] = relationship(
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates="followers",
    )
    followers: WriteOnlyMapped[User] = relationship(
        secondary=followers,
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates="following",
    )

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

    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    def followers_count(self):
        query = select(func.count()).select_from(self.followers.select().subquery())
        return db.session.scalar(query)

    def following_count(self):
        query = select(func.count()).select_from(self.following.select().subquery())
        return db.session.scalar(query)

    def following_posts(self):
        Author = aliased(User)
        Follower = aliased(User)

        return (
            select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), isouter=True)
            .where(
                or_(
                    Follower.id == self.id,
                    Author.id == self.id,
                )
            )
            .group_by(Post.id)
            .order_by(Post.timestamp.desc())
        )


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
