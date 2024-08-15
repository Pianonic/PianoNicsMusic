from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_utils.base import Base

# Create a synchronous engine for the SQLite in-memory database
engine = create_engine('sqlite:///:memory:', echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

async def setup_db():
    # Create the tables in the in-memory SQLite database
    Base.metadata.create_all(bind=engine)

def get_session():
    # Provide a session instance
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
