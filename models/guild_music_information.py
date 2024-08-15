from dataclasses import dataclass
from typing import List
from sqlalchemy import Column, Integer, Boolean
from models.queue_object import QueueEntryDto
from db_utils.base import Base
from sqlalchemy.orm import relationship

class Guild(Base):
  __tablename__ = 'guilds'

  id = Column(Integer, primary_key=True)
  loop_queue = Column(Boolean, nullable=False)
  shuffle_queue = Column(Boolean, nullable=False)
  queue = relationship("QueueEntry", backref="guilds", cascade="all, delete-orphan", lazy="select")

@dataclass
class GuildDto:
  discord_guild_id: int
  loop_queue: bool
  shuffle_queue: bool
  queue: List[QueueEntryDto]

def map(guild: Guild) -> GuildDto:
  queue_dtos = [QueueEntryDto(url=entry.url, already_played=entry.already_played) for entry in guild.queue]
  
  return GuildDto(
    discord_guild_id=guild.id,
    loop_queue=guild.loop_queue,
    shuffle_queue=guild.shuffle_queue,
    queue=queue_dtos
  )