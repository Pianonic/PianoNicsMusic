from peewee import SqliteDatabase
import os

# Use a persistent database file instead of in-memory
db_path = os.path.join(os.path.dirname(__file__), '..', 'bot_data.db')
db = SqliteDatabase(db_path)

async def setup_db():
    try:
        from models.guild_music_information import Guild
        from models.queue_object import QueueEntry

        # Connect to database
        if not db.is_connection_usable():
            db.connect()
        
        # Create tables if they don't exist
        db.create_tables([Guild, QueueEntry], safe=True)
        print("Database setup completed successfully")
    except Exception as e:
        print(f"Error setting up database: {e}")
        raise e