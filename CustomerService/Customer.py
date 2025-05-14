from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    USERNAME = Column(String(50), nullable=False, unique=True)
    FIRSTNAME = Column(String(50), nullable=False)
    LASTNAME = Column(String(50), nullable=False)
    EMAIL = Column(String(100), nullable=False, unique=True)
    PHONE = Column(String(15), nullable=False, unique=True)
    ADDRESS = Column(String(255), nullable=False)
    CITY = Column(String(50), nullable=False)
    STATE = Column(String(2), nullable=False)
    ZIPCODE = Column(String(10), nullable=False)
    HASHED_PASSWORD = Column(String(128), nullable=False)
    DATE_CREATED = Column(TIMESTAMP, server_default=func.now())
    LAST_UPDATED = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.ID,
            "username": self.USERNAME,
            "firstname": self.FIRSTNAME,
            "lastname": self.LASTNAME,
            "email": self.EMAIL,
            "phone": self.PHONE,
            "address": self.ADDRESS,
            "city": self.CITY,
            "state": self.STATE,
            "zipcode": self.ZIPCODE,
        }