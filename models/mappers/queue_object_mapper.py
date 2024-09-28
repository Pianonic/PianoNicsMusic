from models.dtos import QueueEntryDto
from models.queue_object import QueueEntry

def map(queue_entry: QueueEntry) -> QueueEntryDto:
    return QueueEntryDto(
        url=queue_entry.url,
        already_played=queue_entry.already_played
    )
