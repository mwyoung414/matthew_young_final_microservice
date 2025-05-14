from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from States import State




Base = declarative_base()
class StatesDbContext:
    """A class to handle database operations for states."""
    def __init__(self, db_url: str):
        if not db_url:
            raise ValueError("Database URL must be provided.")
        self.engine = create_async_engine(db_url, echo=True)
        self.session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        
    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    async def get_all_states(self):
        """"Get all states from the database."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(State))
                return result.scalars().all()
            
            

            
__all__ = ["StatesDbContext","State"]