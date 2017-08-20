from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base


class Mission(declarative_base()):
    __tablename__ = 'missions'
    id = Column(Integer, primary_key=True)
    payload = Column(JSONB)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
