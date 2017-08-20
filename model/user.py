from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class User(declarative_base()):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    token = Column(String)
    email = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
