from dataclasses import dataclass
from typing import List
from sqlalchemy import Integer, Boolean
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from models import queue_object
from models.queue_object import QueueObject, QueueObjectDto

Base = declarative_base()

class GuildMusicInformation(Base):
    __tablename__ = 'guild_music_information'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_bot_busy: Mapped[bool] = mapped_column(Boolean, default=False)
    loop_queue: Mapped[bool] = mapped_column(Boolean, default=False)
    
    queue: Mapped[List[QueueObject]] = relationship('QueueObject', backref='guild_music_info')

@dataclass
class GuildMusicInformationDto:
  guild_id: int
  is_bot_busy: bool
  queue: List[QueueObjectDto]
  loop_queue: bool


def map(info: GuildMusicInformation) -> GuildMusicInformationDto:
  """Convert GuildMusicInformation to GuildMusicInformationDto."""
  return GuildMusicInformationDto(
      guild_id=info.guild_id,
      is_bot_busy=info.is_bot_busy,
      queue=[queue_object.map(q) for q in info.queue],
      loop_queue=info.loop_queue
  )