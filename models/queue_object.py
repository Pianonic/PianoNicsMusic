from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from db_utils.base import Base

class QueueEntry(Base):
  __tablename__ = 'queue_entry'

  id = Column(Integer, primary_key=True, autoincrement=True)
  guild_id = Column(Integer, ForeignKey("guilds.id"), nullable=False)
  url = Column(String, nullable=False)
  already_played = Column(Boolean, nullable=False)
  force_play = Column(Boolean, nullable=False)

@dataclass
class QueueEntryDto:
  url: str
  already_played: bool

def map(queue_entry: QueueEntry) -> QueueEntryDto:
  return QueueEntryDto(
    url=queue_entry.url,
    already_played=queue_entry.already_played
  )