from dataclasses import dataclass

@dataclass
class MusicInformation:
    streaming_url: str
    song_name: str
    author: str
    image_url: str
