from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(16), unique=True, index=True)
    name = Column(String(25))
    email_id = Column(String(255))
    hashed_password = Column(String(255))
    liked_blogs = Column(String(255), nullable=True)
    # is_created + 3

    @property
    def data_list(self):
        return self.liked_blogs.split(",") if self.liked_blogs else []

    @data_list.setter
    def data_list(self, value):
        self.liked_blogs = ",".join(value)


class Blog(Base):
    __tablename__ = "blogs"

    blog_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    blog_title = Column(String(80))
    blog_summary = Column(String(160))
    blog_content = Column(String(255))
    likes = Column(String(255), nullable=True)
    # is_published, is_updated

    @property
    def data_list(self):
        return self.likes.split(",") if self.likes else []

    @data_list.setter
    def data_list(self, value):
        self.likes = ",".join(value)


#     parent = relationship('User', back_populates='blogs')

# User.children = relationship('Blog', order_by=Blog.blog_id, back_populates='users')
