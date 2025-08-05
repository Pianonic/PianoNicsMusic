"""
Database migration utility for adding volume support to PianoNicsMusic
This script will add the volume column to existing guild tables
"""
import logging
from peewee import SqliteDatabase, DoesNotExist
from models.guild_music_information import Guild

logger = logging.getLogger('PianoNicsMusic')

async def migrate_add_volume_column():
    """Add volume column to existing guilds table if it doesn't exist"""
    try:
        # Check if volume column exists by trying to access it
        test_guild = Guild.select().limit(1).first()
        if test_guild:
            # Try to access volume field - if it exists, migration is not needed
            _ = test_guild.volume
            logger.info("Volume column already exists, migration not needed")
            return True
    except Exception:
        # Volume column doesn't exist, need to add it
        logger.info("Adding volume column to guilds table")
        
        try:
            # Add the volume column with default value
            Guild._meta.database.execute_sql('ALTER TABLE guilds ADD COLUMN volume REAL DEFAULT 1.0')
            
            # Update all existing guilds to have default volume
            Guild.update(volume=1.0).where(Guild.volume.is_null()).execute()
            
            logger.info("Successfully added volume column to guilds table")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add volume column: {e}")
            return False
    
    return True
