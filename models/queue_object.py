from dataclasses import dataclass

@dataclass
class QueueObject:
  url: str
  already_played: bool