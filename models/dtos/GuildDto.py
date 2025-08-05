from dataclasses import dataclass
from models.dtos.QueueEntryDto import QueueEntryDto

@dataclass
class GuildDto:
    discord_guild_id: int
    loop_queue: bool
    shuffle_queue: bool
    volume: float  # Volume level (0.0 to 1.0)
    queue: list[QueueEntryDto]