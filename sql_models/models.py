from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from connection.connection_sql import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    items = relationship("Item", back_populates='owner')
    
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    product_name = Column(String, unique=True, index=True)
    description = Column(String, index = True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")