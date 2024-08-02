from enum import Enum

class AudioContentType(Enum):
    NOT_SUPPORTED = 1
    QUERY = 2
    SINGLE_SONG = 3
    PLAYLIST = 4
    RADIO = 5
    ALBUM = 6
    YT_DLP = 7
    