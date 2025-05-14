from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Admin(Base):
    
    __tablename__ = "admins"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    USERNAME = Column(String(50), nullable=False, unique=True)
    EMAIL = Column(String(100), nullable=False, unique=True)
    HASHED_PASSWORD = Column(String(128), nullable=False)
    DATE_CREATED = Column(TIMESTAMP, server_default=func.now())
    LAST_UPDATED = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    
    def __init__(self, USERNAME: str, EMAIL: str, HASHED_PASSWORD: str):
        # pass those directly to the SQLAlchemy Base
        super().__init__(USERNAME=USERNAME,
                         EMAIL=EMAIL,
                         HASHED_PASSWORD=HASHED_PASSWORD)

    def to_dict(self):
        return {
            "id": self.ID,
            "username": self.USERNAME,
            "email": self.EMAIL,
        }