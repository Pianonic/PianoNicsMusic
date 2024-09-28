import random
from typing import List
from models.dtos.QueueEntryDto import QueueEntryDto
from models.dtos.GuildDto import GuildDto
from models.guild_music_information import Guild
from models.queue_object import QueueEntry
from models.mappers import guild_music_information_mapper

async def create_new_guild(discord_guild_id: int):
    Guild.create(id=discord_guild_id, loop_queue=False, shuffle_queue=False)

async def get_guild(discord_guild_id: int) -> GuildDto | None: 
    guild = Guild.get_or_none(Guild.id == discord_guild_id)
    if guild:
        return guild_music_information_mapper.map(guild)
    return None

async def delete_queue(guild_id: int):
    QueueEntry.delete().where(QueueEntry.guild == guild_id).execute()

async def add_to_queue(guild_id: int, song_urls: List[str]):
    queue_entries = [QueueEntry(guild=guild_id, url=url, already_played=False, force_play=False) for url in song_urls]
    QueueEntry.bulk_create(queue_entries)

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

async def _set_all_entrys_as_not_listened(guild_id: int):
    QueueEntry.update(already_played=False).where(QueueEntry.guild == guild_id).execute()

async def _mark_entry_as_listened(entry: QueueEntry):
    entry.already_played = True
    entry.force_play = False
    entry.save()

async def get_queue_entry(guild_id: int) -> str | None:
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
        entry = QueueEntry.select().where((QueueEntry.guild == guild_id) & (QueueEntry.already_played == False)).order_by(QueueEntry.id).first()



    if entry:
        await _mark_entry_as_listened(entry)
        return entry.url
    elif not entry and guild.loop_queue:
        # if loop is active
        await _set_all_entrys_as_not_listened(guild_id)
        return await get_queue_entry(guild_id)
    else:
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