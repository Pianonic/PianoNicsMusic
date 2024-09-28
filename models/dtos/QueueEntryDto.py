from dataclasses import dataclass

@dataclass
class QueueEntryDto:
    url: str
    already_played: bool