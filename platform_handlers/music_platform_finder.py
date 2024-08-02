from urllib.parse import urlsplit
from enums.platform import Platform

async def find_platform(query_url: str) -> Platform:
    split_url = urlsplit(query_url)
    hostname = split_url.hostname

    if not hostname:
        return Platform.NO_URL

    elif "spotify" in hostname:
        return Platform.SPOTIFY

    elif "tiktok" in hostname:
        return Platform.TIK_TOK

    elif "youtube" in hostname or "youtu" in hostname:
        return Platform.YOUTUBE

    elif "soundcloud" in hostname:
        return Platform.SOUND_CLOUD

    else:
        return Platform.ANYTHING_ELSE