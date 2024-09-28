from peewee import SqliteDatabase

db = SqliteDatabase(':memory:')

async def setup_db():
    from models.guild_music_information import Guild
    from models.queue_object import QueueEntry

    db.create_tables([Guild, QueueEntry])