from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from bluelog.extensions import db


class Admin(db.Model, UserMixin):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(20), unique=True)
    password_hash = mapped_column(String(128))
    blog_title = mapped_column(String(60))
    blog_sub_title = mapped_column(String(100))
    name = mapped_column(String(30))
    about = mapped_column(Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(30), unique=True)

    posts = relationship("Post", back_populates="category")


class Post(db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String(60))
    body = mapped_column(Text)
    timestamp = mapped_column(DateTime, default=datetime.utcnow)
    can_comment = mapped_column(Boolean, default=True)

    category_id = mapped_column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="posts")

    comments = relationship("Comment", backref="post", cascade="all")


class Comment(db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    author = mapped_column(String(30))
    email = mapped_column(String(254))
    site = mapped_column(String(255))
    body = mapped_column(Text)
    from_admin = mapped_column(Boolean, default=False)
    reviewed = mapped_column(Boolean, default=False)
    timestamp = mapped_column(DateTime, default=datetime.utcnow, index=True)

    post_id = mapped_column(Integer, ForeignKey("post.id"))
    # post = relationship("Post", back_populates="comments")  # 加了会报错 后面来分析一下

    replied_id = mapped_column(Integer, ForeignKey("comment.id"))
    replied = relationship("Comment", back_populates="replies", remote_side=[id])
    replies = relationship("Comment", back_populates="replied", cascade="all")
