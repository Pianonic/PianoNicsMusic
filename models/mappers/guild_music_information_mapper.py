from models.guild_music_information import Guild
from models.queue_object import QueueEntry
from models.dtos.GuildDto import GuildDto
from models.dtos.QueueEntryDto import QueueEntryDto

def map(guild: Guild) -> GuildDto:
    queue_entries = QueueEntry.select().where(QueueEntry.guild == guild)
    queue_dtos = [QueueEntryDto(url=entry.url, already_played=entry.already_played) for entry in queue_entries]
    
    return GuildDto(
        discord_guild_id=guild.id,
        loop_queue=guild.loop_queue,
        shuffle_queue=guild.shuffle_queue,
        volume=guild.volume,
        queue=queue_dtos
    )