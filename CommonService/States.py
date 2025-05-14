from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class State(Base):
    __tablename__ = "states"
    code = Column(String(2), nullable=False, unique=True, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    