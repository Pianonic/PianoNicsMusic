from urllib.parse import urlsplit
from enums.source import Source

async def find_music_source(query_url: str) -> Source:
    split_url = urlsplit(query_url)
    hostname = split_url.hostname

    if not hostname:
        return Source.NO_URL

    elif "spotify" in hostname:
        return Source.SPOTIFY

    elif "tiktok" in hostname:
        return Source.TIK_TOK

    elif "youtube" in hostname or "youtu" in hostname:
        return Source.YOUTUBE

    elif "soundcloud" in hostname:
        return Source.SOUND_CLOUD

    else:
        return Source.UNKNOWN_SOURCE