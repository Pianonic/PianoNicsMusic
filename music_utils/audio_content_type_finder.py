from enums.audio_content_type import AudioContentType
from enums.source import Source
import requests

from urllib.parse import urlparse
from urllib.parse import parse_qs

import music_utils.music_source_finder as MSF


async def get_audio_content_type(query_url: str, source: Source = None) -> AudioContentType:
    if source is None:
        source = await MSF.find_music_source(query_url)

    if source is Source.YOUTUBE:
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
    
    elif source is Source.SOUND_CLOUD:
        parse_result = urlparse(query_url)
        path = parse_result.path
        path_segments = path.strip("/").split("/")

        if "sets" in path_segments:
            return AudioContentType.PLAYLIST
        else:
            return AudioContentType.SINGLE_SONG
    
    elif source is Source.SPOTIFY:
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

    elif source is Source.TIK_TOK:
        return AudioContentType.SINGLE_SONG
    
    elif source is Source.NO_URL:
        return AudioContentType.QUERY
    
    elif source is Source.UNKNOWN_SOURCE:
        response = requests.get(query_url)
        contentType = response.headers['content-type']

        if "audio" in contentType or "video" in contentType:
            return AudioContentType.SINGLE_SONG
        else:
            return AudioContentType.YT_DLP
        
    else:
        raise Exception("Error determining the audio content type.")