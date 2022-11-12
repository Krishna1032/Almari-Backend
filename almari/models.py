from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    phone_number = Column(String, nullable = True)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    

class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    category = Column(String, nullable = False)
    title = Column(String, nullable = False)
    description = Column(String, nullable = False)
    price = Column(Integer, nullable = False)
    post_img = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone= True), nullable = False, server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable = False)
    owner = relationship("Users")

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key = True, nullable = False)
    quantity = Column(Integer, nullable = False)
    product_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), nullable = False, unique = True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable = False)
    owner = relationship("Users")
    product = relationship("Posts")
