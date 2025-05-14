from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from Booking import Booking, Base

class BookingDbContext:
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
        
    async def add_booking(self, booking: Booking):
        """Add a new booking to the database."""
        async with self.session() as session:
            async with session.begin():
                session.add(booking)
                await session.commit()
                await session.refresh(booking)
                return booking.ID
            
    async def get_booking(self, param: str, value: str):
        """Get a booking by a specific parameter."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Booking).where(getattr(Booking, param) == value))
                return result.scalars().first()
            
    async def get_booking_by_user_id(self, user_id: int):
        """Get a booking by user ID."""
        return await self.get_booking("USER_ID", user_id)
    
    async def get_all_bookings(self):
        """Get all bookings from the database."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Booking))
                return result.scalars().all()
    
    