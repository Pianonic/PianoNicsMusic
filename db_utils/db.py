from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.guild_music_information import Base as GuildMusicBase
from models.queue_object import Base as QueueObjectBase

# Create an asynchronous engine for the SQLite in-memory database
# Use 'sqlite+aiosqlite:///:memory:' for in-memory SQLite
engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)

# Create a configured "AsyncSession" class
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def setup_db():
    """
    Asynchronously sets up the database and creates all tables.
    """
    async with engine.begin() as conn:
        # Run the table creation in a transaction
        await conn.run_sync(GuildMusicBase.metadata.create_all)
        await conn.run_sync(QueueObjectBase.metadata.create_all)

def get_session() -> AsyncSession:
    """
    Returns a new async session instance for database interactions.
    Remember to close the session after use to free up resources.
    """
    return AsyncSessionLocal()