from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from Transaction import Transaction, Base



class TransactionsDbContext():
    def __init__(self, db_url: str):
        if not db_url:
            raise ValueError("Database URL must be provided.")
        self.engine = create_async_engine(db_url, echo=True)
        self.session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        
    async def init_db(self):
        async with self.engine.begin() as conn:
            # Create the table
            await conn.run_sync(Base.metadata.create_all)
            
    async def get_all_transactions(self):
        """Get all transactions from the database."""
        async with self.session() as session:
            async with session.begin():
                result = await session.execute(select(Transaction))
                return result.scalars().all()
            
    async def add_transaction(self, transaction: Transaction):
        """Add a new transaction to the database."""
        async with self.session() as session:
            async with session.begin():
                session.add(transaction)
                await session.commit()
                return transaction.id
            
    