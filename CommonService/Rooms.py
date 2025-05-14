from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Room(Base):
    __tablename__ = "rooms"
    id = Column(String(50), primary_key=True)
    room_type = Column(String(50), nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "room_type": self.room_type,
            "price": self.price,
        }