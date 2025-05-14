from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from Admin import Admin, Base

class AdminDbContext():
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
            
    async def add_admin(self, admin:Admin):
        """Add a new admin to the database."""
        async with self.session() as session:
            async with session.begin():
                session.add(admin)
                await session.commit()
                await session.refresh(admin)
                return admin.ID
                
    async def get_admin(self, param: str, value: str):
        """Get an admin by a specific parameter."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Admin).where(getattr(Admin, param) == value))
                return result.scalars().first()
            
    async def get_admin_by_id(self, id: int):
        """Get an admin by ID."""
        return await self.get_admin("ID", id)
    
    async def get_all_admins(self):
        """Get all admins."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Admin))
                admins = result.scalars().all()
                return [admin.to_dict() for admin in admins]
            
    async def update_admin(self, id: int, **kwargs):
        """Update an admin by ID."""
        async with self.session() as session:
            async with session.begin():
                admin = await self.get_admin_by_id(id)
                if admin:
                    for key, value in kwargs.items():
                        setattr(admin, key, value)
                    await session.commit()
                    return True
                return False
            
    async def delete_admin(self, id: int):
        """Delete an admin by ID."""
        async with self.session() as session:
            async with session.begin():
                admin = await self.get_admin_by_id(id)
                if admin:
                    await session.delete(admin)
                    await session.commit()
                    return True
                return False
