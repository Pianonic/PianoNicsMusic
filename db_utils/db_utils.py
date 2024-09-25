import random
from typing import List
from db_utils.db import get_session
from models.guild_music_information import Guild, GuildDto
from models import guild_music_information
from models.queue_object import QueueEntry, QueueEntryDto
from sqlalchemy import delete

async def create_new_guild(discord_guild_id: int):
    for session in get_session():
        with session.begin():
            guild_instance = Guild(id=discord_guild_id, loop_queue=False, shuffle_queue=False)
            session.add(guild_instance)
        session.commit()

async def get_guild(discord_guild_id: int) -> GuildDto | None:
    for session in get_session():
        with session.begin():
            guild_instance = session.query(Guild).filter_by(id=discord_guild_id).first()
            
            if guild_instance:
                return guild_music_information.map(guild_instance)
    return None

async def delete_queue(guild_id: int):
    for session in get_session():
        with session.begin():
            session.query(QueueEntry).filter_by(guild_id=guild_id).delete(synchronize_session='fetch')
        session.commit()

async def add_to_queue(guild_id: int, song_urls: List[str]):
    for session in get_session():
        with session.begin():
            queue_entries = [QueueEntry(url=url, already_played=False, force_play=False) for url in song_urls]
            for queue_object in queue_entries:
                queue_object.guild_id = guild_id
                session.add(queue_object)
        session.commit()

async def add_force_next_play_to_queue(guild_id: int, song_url: str):
    for session in get_session():
        with session.begin():
            session.add(QueueEntry(url=song_url, already_played=False, force_play=True, guild_id=guild_id))
        session.commit()

async def delete_guild(discord_guild_id: int):
    for session in get_session():
        with session.begin():
            session.query(Guild).filter_by(id=discord_guild_id).delete(synchronize_session='fetch')
        session.commit()

async def get_queue(guild_id: int) -> List[QueueEntryDto]:
    for session in get_session():
        with session.begin():
            queue_entries = session.query(QueueEntry).filter_by(guild_id=guild_id).all()
            queue_dtos = [QueueEntryDto(url=entry.url, already_played=entry.already_played) for entry in queue_entries]
            
            return queue_dtos
        
async def get_queue_entry(guild_id: int) -> str | None:
    for session in get_session():
        with session.begin():
            guild = session.query(Guild).filter_by(id=guild_id).first()
            if not guild:
                return None
            
            force_queue_entry = session.query(QueueEntry).filter_by(guild_id=guild_id, already_played=False, force_play=True).first()
            if force_queue_entry:
                url: str = force_queue_entry.url
                force_queue_entry.already_played = True
                force_queue_entry.force_play = False
                session.add(force_queue_entry)
                session.commit()
                return url
            
            if guild.shuffle_queue:
                queue_entries = session.query(QueueEntry).filter_by(guild_id=guild_id, already_played=False).all()
                if not queue_entries:
                    return None
                selected_entry = random.choice(queue_entries)
            else:
                selected_entry = session.query(QueueEntry).filter_by(guild_id=guild_id, already_played=False).order_by(QueueEntry.id).first()
                if not selected_entry:
                    return None

            url: str = selected_entry.url
            selected_entry.already_played = True
            selected_entry.force_play = False
            session.add(selected_entry)
            session.commit()
            return url
        
async def shuffle_playlist(guild_id: int):
    for session in get_session():
        with session.begin():
            guild = session.query(Guild).filter_by(id=guild_id).first()
            
            if not guild:
                return None
            
            guild.shuffle_queue = True
            
            session.add(guild)
            session.commit()