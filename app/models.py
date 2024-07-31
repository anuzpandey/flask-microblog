from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc), nullable=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(256))
    body: so.Mapped[str] = so.mapped_column(sa.String(4096))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='posts')
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc), nullable=True)

    def __repr__(self):
        return '<Post {}>'.format(self.title)
