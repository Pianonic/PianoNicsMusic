from peewee import SqliteDatabase

db = SqliteDatabase(':memory:')

async def setup_db():
    try:
        from models.guild_music_information import Guild
        from models.queue_object import QueueEntry

        # Connect to database
        if not db.is_connection_usable():
            db.connect()
        
        # Create tables if they don't exist
        db.create_tables([Guild, QueueEntry], safe=True)
        print("In-memory database setup completed successfully")
    except Exception as e:
        print(f"Error setting up database: {e}")
        raise e