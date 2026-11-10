from datetime import datetime
from sqlalchemy.orm import Relationship
from  database import *
import models
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text, ForeignKey


# class Post(Base):
#     __tablename__ = "posts"
#     # SQLAlchemy automatically treats a single-column integer primary key as an auto-incrementing column by default.
#     id = Column('id', Integer, primary_key=True, nullable=False)
#     title = Column('title', String, nullable=False)
#     content = Column('content', String, nullable=False)
#     published = Column('published', Boolean, default=True)

class Post(Base):
    __tablename__ = "posts" 
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    
    '''
        defines an ORM relationship, which acts as a virtual link or shortcut between your Python classes.
        # SQLAlchemy automatically fetches the user under the hood
            print(post.owner.email)  # Outputs: admin@gmail.com
            print(post.owner.id)     # Outputs: 1
        
    '''
    # Links related post to its single owner (User object)
    # owner: Mapped["User"] = Relationship("User", back_populates="posts")
    owner = Relationship("User")
    
    votes = Relationship("Vote")
    
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_num: Mapped[str]

class Vote(Base):
    __tablename__ = "votes"
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"),nullable=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),nullable=False, primary_key=True)
    
    
    
# Automatically create tables on application startup.
# Base.metadata.drop_all(engine)
# models.Base.metadata.create_all(bind=engine)

