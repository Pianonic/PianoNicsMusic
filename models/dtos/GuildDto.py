from dataclasses import dataclass
from models.dtos.QueueEntryDto import QueueEntryDto

@dataclass
class GuildDto:
    discord_guild_id: int
    loop_queue: bool
    shuffle_queue: bool
    queue: list[QueueEntryDto]