from sqlalchemy import create_engine, MetaData

# Create an in-memory SQLite database
engine = create_engine('sqlite:///:memory:', echo=True)

# Create a metadata object
meta = MetaData()

# Create all tables in the database
meta.create_all(engine)
