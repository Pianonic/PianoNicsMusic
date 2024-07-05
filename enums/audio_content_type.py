from enum import Enum

class AudioContentType(Enum):
    NOT_SUPPORTED = 1
    SINGLE_SONG = 2
    PLAYLIST = 3
    RADIO = 4
    ALBUM = 5
    