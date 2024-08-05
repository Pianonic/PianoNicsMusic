
from sqlalchemy.future import select
from sqlalchemy import delete
from db_utils.db import get_session
from models.guild_music_information import GuildMusicInformation, GuildMusicInformationDto, map
from models.queue_object import QueueObject
from typing import List, Optional


async def get_guild_object(guild_id: int) -> Optional[GuildMusicInformationDto]:
    """
    Asynchronously retrieves a GuildMusicInformationDto object by guild_id.
    """
    async with get_session() as session:
        result = await session.execute(select(GuildMusicInformation).where(GuildMusicInformation.guild_id == guild_id))
        guild_info = result.scalars().first()

        if guild_info:
            return map(guild_info)
        return None

async def delete_queue(guild_id: int):
    """
    Asynchronously deletes all QueueObject entries for a given guild_id.
    """
    async with get_session() as session:
        await session.execute(
            delete(QueueObject).where(QueueObject.guild_music_info_id == guild_id)
        )
        await session.commit()

async def delete_guild(guild_id: int):
    """
    Asynchronously deletes a GuildMusicInformation entry and its related QueueObjects for a given guild_id.
    """
    async with get_session() as session:
        await session.execute(delete(QueueObject).where(QueueObject.guild_music_info_id == guild_id))
        await session.execute(delete(GuildMusicInformation).where(GuildMusicInformation.guild_id == guild_id))
        await session.commit()

async def create_new_guild_music_information(guild_id: int) -> GuildMusicInformationDto:
    """
    Asynchronously creates a new GuildMusicInformation entry and returns it as a DTO.
    """
    async with get_session() as session:
        new_guild_info = GuildMusicInformation(guild_id=guild_id, is_bot_busy=False, loop_queue=False)
        session.add(new_guild_info)
        await session.commit()
        await session.refresh(new_guild_info)  # Refresh to get the new ID

        return map(new_guild_info)

async def add_to_queue(guild_id: int, queue_object_list: List[QueueObject]):
    """
    Asynchronously adds a list of QueueObjects to the queue of a given guild_id.
    """
    async with get_session() as session:
        for queue_object in queue_object_list:
            queue_object.guild_music_info_id = guild_id
            session.add(queue_object)
        await session.commit()