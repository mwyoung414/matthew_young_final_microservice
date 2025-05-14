from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text
from Rooms import Room

Base = declarative_base()

class RoomsDbContext():
    def __init__(self, db_url: str):
        if not db_url:
            raise ValueError("Database URL must be provided.")
        self.engine = create_async_engine(db_url, echo=True)
        self.session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        
    async def init_db(self):
        async with self.engine.begin() as conn:
            # Create the table
            await conn.execute(text(
                """
                CREATE TABLE IF NOT EXISTS rooms (
                    id SERIAL PRIMARY KEY,
                    room_type VARCHAR(50) UNIQUE NOT NULL,
                    price NUMERIC(10, 2) NOT NULL
                );
                """
            ))
        # Check if table is empty before inserting
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Room))
                if not result.scalars().first():
                    await session.execute(text("INSERT INTO rooms (room_type, price) VALUES ('Queen', 100.00)"))
                    await session.execute(text("INSERT INTO rooms (room_type, price) VALUES ('King', 200.00)"))
                    await session.execute(text("INSERT INTO rooms (room_type, price) VALUES ('Suite', 400.00)"))
                    await session.execute(text("INSERT INTO rooms (room_type, price) VALUES ('Presidential', 1000.00)"))
                    await session.commit()
            
    async def get_all_rooms(self):
        """"Get all rooms from the database."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Room))
                return result.scalars().all()
            
    async def get_price_by_type(self, type: str):
        """Get the price of a room by type."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Room).where(Room.room_type == type))
                return result.scalars().first()