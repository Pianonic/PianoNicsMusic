from dataclasses import dataclass
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class QueueObject(Base):
    __tablename__ = 'queue_objects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    already_played: Mapped[bool] = mapped_column(Boolean, default=False)
    guild_music_info_id: Mapped[int] = mapped_column(Integer, ForeignKey('guild_music_information.id'))

@dataclass
class QueueObjectDto:
  url: str
  already_played: bool

def map(queue_object: QueueObject) -> QueueObjectDto:
    """Convert QueueObject to QueueObjectDto."""
    return QueueObjectDto(
        url=queue_object.url,
        already_played=queue_object.already_played
    )