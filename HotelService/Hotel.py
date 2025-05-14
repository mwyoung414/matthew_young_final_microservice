from sqlalchemy import Column, Integer, String, TEXT
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Hotel(Base):
    __tablename__ = "hotels"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    HOTELNAME = Column(String(100), nullable=False)
    HOTELRATING = Column(Integer, nullable=False)
    ADDRESS = Column(String(255), nullable=False)
    CITY = Column(String(100), nullable=False)
    STATE = Column(String(2), nullable=False)
    DESCRIPTION = Column(TEXT, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.ID,
            "name": self.HOTELNAME,
            "rating": self.HOTELRATING,
            "address": self.ADDRESS,
            "city": self.CITY,
            "state": self.STATE,
            "description": self.DESCRIPTION
        }