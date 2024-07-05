from platform_handlers.audio_content_type_finder import get_audio_content_type

from urllib.parse import urlsplit
from enums.platform import Platform

def find_platform(query_url: str) -> Platform:
    split_url = urlsplit(query_url)
    hostname = split_url.hostname

    if "spotify" in hostname:
        return Platform.SPOTIFY

    elif "tiktok" in hostname:
        return Platform.TIK_TOK

    else:
        return Platform.ANYTHING_ELSE

async def get_streaming_url(query_url: str):
    platform = find_platform(query_url)
    audio_content_type = get_audio_content_type(query_url, platform)
    return "a" 
