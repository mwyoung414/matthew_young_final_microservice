from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from Customer import Customer, Base


class CustomerDbContext():
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
            
    async def add_customer(self, Customer:Customer):
        """Add a new customer to the database."""
        async with self.session() as session:
            async with session.begin():
                session.add(Customer)
                await session.commit()
                await session.refresh(Customer)
                return Customer.ID
                
    async def get_customer(self, param: str, value: str):
        """Get a customer by a specific parameter."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Customer).where(getattr(Customer, param) == value))
                return result.scalars().first()
            
    async def get_customer_by_id(self, id: int):
        """Get a customer by ID."""
        return await self.get_customer("ID", id)
    
    async def get_customer_by_email(self, email: str):
        """Get a customer by email."""
        return await self.get_customer("EMAIL", email)
    
    async def get_customer_by_username(self, username: str):
        """Get a customer by username."""
        return await self.get_customer("USERNAME", username)
    
    async def delete_customer(self, id: int):
        """Delete a customer by ID."""
        async with self.session() as session:
            async with session.begin():
                customer = await self.get_customer_by_id(id)
                if customer:
                    await session.delete(customer)
                    await session.commit()
                    return True
                return False
            
    async def update_customer(self, id: int, **kwargs):
        """Update a customer's information."""
        async with self.session() as session:
            async with session.begin():
                customer = await self.get_customer_by_id(id)
                if customer:
                    for key, value in kwargs.items():
                        setattr(customer, key, value)
                    await session.commit()
                    return True
                return False
            
    async def get_all_customers(self):
        """Get all customers from the database."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Customer))
                customers = result.scalars().all()
                return [customer.to_dict() for customer in customers]
            
__all__ = ["CustomerDbContext", "Customer"]
