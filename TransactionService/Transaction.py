from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    hotel_id = Column(Integer, nullable=False)
    room_type = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, customer_id={self.customer_id}, hotel_id={self.hotel_id}, room_type={self.room_type}, price={self.price}, status={self.status}, created_at={self.created_at})>"