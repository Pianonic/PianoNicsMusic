import random
from typing import List
from models.dtos.QueueEntryDto import QueueEntryDto
from models.dtos.GuildDto import GuildDto
from models.guild_music_information import Guild
from models.queue_object import QueueEntry
from models.mappers import guild_music_information_mapper

async def create_new_guild(discord_guild_id: int):
    try:
        Guild.create(id=discord_guild_id, loop_queue=False, shuffle_queue=False)
    except Exception as e:
        print(f"Error creating guild {discord_guild_id}: {e}")
        # Try to get existing guild if creation failed
        existing_guild = Guild.get_or_none(Guild.id == discord_guild_id)
        if not existing_guild:
            raise e

async def get_guild(discord_guild_id: int) -> GuildDto | None: 
    try:
        guild = Guild.get_or_none(Guild.id == discord_guild_id)
        if guild:
            return guild_music_information_mapper.map(guild)
        return None
    except Exception as e:
        print(f"Error getting guild {discord_guild_id}: {e}")
        return None

async def delete_queue(guild_id: int):
    try:
        QueueEntry.delete().where(QueueEntry.guild == guild_id).execute()
    except Exception as e:
        print(f"Error deleting queue for guild {guild_id}: {e}")
        # Continue anyway, this is cleanup

async def add_to_queue(guild_id: int, song_urls: List[str]):
    try:
        if not song_urls:
            return
        queue_entries = [QueueEntry(guild=guild_id, url=url, already_played=False, force_play=False) for url in song_urls]
        QueueEntry.bulk_create(queue_entries)
    except Exception as e:
        print(f"Error adding songs to queue for guild {guild_id}: {e}")
        # Try adding one by one if bulk create fails
        try:
            for url in song_urls:
                QueueEntry.create(guild=guild_id, url=url, already_played=False, force_play=False)
        except Exception as e2:
            print(f"Error adding songs individually: {e2}")
            raise e2

async def add_force_next_play_to_queue(guild_id: int, song_url: str):
    QueueEntry.create(guild=guild_id, url=song_url, already_played=False, force_play=True)

async def delete_guild(discord_guild_id: int):
    Guild.delete_by_id(discord_guild_id)

async def get_queue(guild_id: int) -> List[QueueEntryDto]:
    queue_entries = QueueEntry.select().where(QueueEntry.guild == guild_id)
    queue_dtos = [QueueEntryDto(url=entry.url, already_played=entry.already_played) for entry in queue_entries]
    return queue_dtos

async def _get_random_queue_entry(guild_id: int) -> str | None:
    queue_entries = QueueEntry.select().where((QueueEntry.guild == guild_id) & (QueueEntry.already_played == False))
    if not queue_entries:
        return None
    return random.choice(list(queue_entries))

async def _mark_entry_as_listened(entry: QueueEntry):
    try:
        entry.already_played = True
        entry.force_play = False
        entry.save()
    except Exception as e:
        print(f"Error marking entry as listened: {e}")
        # This is not critical, continue anyway

async def get_queue_entry(guild_id: int) -> str | None:
    try:
        guild: Guild | None = Guild.get_or_none(Guild.id == guild_id)
        if not guild:
            return None
        
        force_play_entry = QueueEntry.get_or_none(
            (QueueEntry.guild == guild_id) & 
            (QueueEntry.already_played == False) & 
            (QueueEntry.force_play == True)
        )

        if force_play_entry:
            entry = force_play_entry
        
        elif guild.shuffle_queue:
            entry = await _get_random_queue_entry(guild_id)

        else:
            entry = QueueEntry.select().where(
                (QueueEntry.guild == guild_id) & 
                (QueueEntry.already_played == False)
            ).order_by(QueueEntry.id).first()

        if entry:
            await _mark_entry_as_listened(entry)
            return entry.url
        
        if guild.loop_queue:
            try:
                QueueEntry.update(already_played=False).where(QueueEntry.guild == guild_id).execute()
                return await _get_entry_after_reset(guild_id)
            except Exception as e:
                print(f"Error resetting queue for guild {guild_id}: {e}")
                return None
        
        return None
    except Exception as e:
        print(f"Error getting queue entry for guild {guild_id}: {e}")
        return None

async def _get_entry_after_reset(guild_id: int) -> str | None:
    guild: Guild | None = Guild.get_or_none(Guild.id == guild_id)
    if not guild:
        return None

    force_play_entry = QueueEntry.get_or_none(
        (QueueEntry.guild == guild_id) & 
        (QueueEntry.already_played == False) & 
        (QueueEntry.force_play == True)
    )

    if force_play_entry:
        entry = force_play_entry
    
    elif guild.shuffle_queue:
        entry = await _get_random_queue_entry(guild_id)

    else:
        entry = QueueEntry.select().where(
            (QueueEntry.guild == guild_id) & 
            (QueueEntry.already_played == False)
        ).order_by(QueueEntry.id).first()

    if entry:
        await _mark_entry_as_listened(entry)
        return entry.url
    
    return None

async def shuffle_playlist(guild_id: int) -> bool:
    guild: Guild | None = Guild.get_or_none(Guild.id == guild_id)
    if not guild:
        return None
    
    guild.shuffle_queue = not guild.shuffle_queue
    guild.save()
    
    return guild.shuffle_queue

async def toggle_loop(guild_id: int) -> bool:
    guild: Guild | None = Guild.get_or_none(Guild.id == guild_id)
    if not guild:
        return None
    
    guild.loop_queue = not guild.loop_queue
    guild.save()
    
    return guild.loop_queue