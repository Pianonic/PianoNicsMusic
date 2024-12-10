from enums.audio_content_type import AudioContentType
from enums.source import Source
import requests

from urllib.parse import urlparse
from urllib.parse import parse_qs

async def get_audio_content_type(query_url: str, platform: Source) -> AudioContentType:
    if platform is Source.YOUTUBE:
        parse_result = urlparse(query_url)
        query_params = parse_qs(parse_result.query)
        result = query_params.get("list", [None])[0]

        if result:
            if result.startswith('RD'):
                return AudioContentType.RADIO
            else:
                return AudioContentType.PLAYLIST
        else:
            return AudioContentType.SINGLE_SONG
    
    elif platform is Source.SOUND_CLOUD:
        parse_result = urlparse(query_url)
        path = parse_result.path
        path_segments = path.strip("/").split("/")

        if "sets" in path_segments:
            return AudioContentType.PLAYLIST
        else:
            return AudioContentType.SINGLE_SONG
    
    elif platform is Source.SPOTIFY:
        parse_result = urlparse(query_url)
        path = parse_result.path
        path_segments = path.strip("/").split("/")

        if "playlist" in path_segments:
            return AudioContentType.PLAYLIST
        elif "album" in path_segments:
            return AudioContentType.ALBUM
        elif "track" in path_segments:
            return AudioContentType.SINGLE_SONG
        else:
            return AudioContentType.NOT_SUPPORTED

    elif platform is Source.NO_URL:
        return AudioContentType.QUERY
    
    elif platform is Source.UNKNOWN_SOURCE:
        response = requests.get(query_url)
        contentType = response.headers['content-type']

        if "audio" in contentType or "video" in contentType:
            return AudioContentType.SINGLE_SONG
        else:
            return AudioContentType.YT_DLP
    
    elif platform is Source.TIK_TOK:
        return AudioContentType.SINGLE_SONG

    else:
        return AudioContentType.NOT_SUPPORTED