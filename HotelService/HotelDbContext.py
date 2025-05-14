from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func
from Hotel import Hotel, Base
import pandas as pd

class HotelDbContext():
    def __init__(self, db_url: str):
        if not db_url:
            raise ValueError("Database URL must be provided.")
        self.engine = create_async_engine(db_url, echo=True)
        self.session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        
    
    async def init_db(self):
        print("Starting database initialization...")
        async with self.engine.begin() as conn:
            print("Creating all tables...")
            await conn.run_sync(Base.metadata.create_all)
        print("Database initialization complete.")
            
    async def add_hotel(self, hotel:Hotel):
        """Add a new hotel to the database."""
        async with self.session() as session:
            async with session.begin():
                session.add(hotel)
                await session.commit()
                await session.refresh(hotel)
                return hotel.ID
                
    async def get_hotel(self, param: str, value: str):
        """Get a hotel by a specific parameter."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Hotel).where(getattr(Hotel, param) == value))
                return result.scalars().first()
            
    async def get_hotel_by_id(self, id: int):
        """Get a hotel by ID."""
        return await self.get_hotel("ID", id)
    
    async def get_all_hotels(self):
        """Get all hotels."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Hotel))
                return result.scalars().all()
            
    async def update_hotel(self, id: int, **kwargs):
        """Update a hotel by ID."""
        async with self.session() as session:
            async with session.begin():
                hotel = await self.get_hotel_by_id(id)
                if hotel:
                    for key, value in kwargs.items():
                        setattr(hotel, key, value)
                    await session.commit()
                    return True
                return False
            
    async def delete_hotel(self, id: int):
        """Delete a hotel by ID."""
        async with self.session() as session:
            async with session.begin():
                hotel = await self.get_hotel_by_id(id)
                if hotel:
                    await session.delete(hotel)
                    await session.commit()
                    return True
                return False
            
    async def seed_from_parquet(self, file_path: str):
        """Seed the database from the first 20 records of a Parquet file."""
        
        df = pd.read_parquet(file_path).head(20)  # Limit to the first 20 records
        async with self.session() as session:
            async with session.begin():
                for _, row in df.iterrows():
                    hotel = Hotel(
                        NAME=row['name'],
                        HOTELRATING=row['rating'],
                        ADDRESS=row['address'],
                        CITY=row['city'],
                        STATE=row['state'],
                        DESCRIPTION=row['description']
                    )
                    session.add(hotel)
                await session.commit()
                await session.refresh(hotel)
        