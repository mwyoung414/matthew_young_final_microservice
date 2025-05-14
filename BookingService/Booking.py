from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Booking(Base):
    __tablename__ = "bookings"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    CUSTOMER_ID = Column(Integer, nullable=False)
    HOTEL_ID = Column(Integer, nullable=False)
    ROOM_TYPE = Column(Integer, nullable=False)
    NUM_OF_ROOMS = Column(Integer, nullable=False)
    TOTAL_PRICE = Column(Integer, nullable=False)
    CHECK_IN_DATE = Column(DateTime, nullable=False)
    CHECK_OUT_DATE = Column(DateTime, nullable=False)
    NUMBER_OF_NIGHTS = Column(Integer, nullable=False)
    DATE_CREATED = Column(DateTime, server_default=func.now())
    
    def to_dict(self):
        return {
            "id": self.ID,
            "user_id": self.USER_ID,
            "hotel_id": self.HOTEL_ID,
            "room_type": self.ROOM_TYPE,
            "num_of_rooms": self.NUM_OF_ROOMS,
            "total_price": self.TOTAL_PRICE,
            "check_in_date": self.CHECK_IN_DATE,
            "check_out_date": self.CHECK_OUT_DATE,
            "number_of_nights": self.NUMBER_OF_NIGHTS,
            "date_created": self.DATE_CREATED
        }