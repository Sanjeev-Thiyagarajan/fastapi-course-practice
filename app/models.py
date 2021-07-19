from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)


# class Vote(Base):
#     __tablename__ = "votes"
#     user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
#     post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
