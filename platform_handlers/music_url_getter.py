from typing import List
from platform_handlers.audio_content_type_finder import get_audio_content_type
from platform_handlers.music_platform_finder import find_platform
from enums.audio_content_type import AudioContentType
from enums.platform import Platform
import yt_dlp
import ytmusicapi

async def get_streaming_url(query_url: str):
    platform = await find_platform(query_url)
    audio_content_type = get_audio_content_type(query_url, platform)
    return "a" 

async def get_urls(query: str) -> List[str]:
    platform = await find_platform(query)
    audio_content_type = await get_audio_content_type(query, platform)

    if audio_content_type is AudioContentType.NOT_SUPPORTED:
        return []
    
    elif audio_content_type is AudioContentType.QUERY:
        yt = ytmusicapi.YTMusic()
        video_id = yt.search(query)[0]["videoId"]
        yt_music_url = f"https://music.youtube.com/watch?v={video_id}"
        return [yt_music_url]
    
    elif audio_content_type is AudioContentType.SINGLE_SONG:
        return [query]
    
    elif audio_content_type is AudioContentType.PLAYLIST or audio_content_type is AudioContentType.RADIO:
        ydl_opts = {
            'extract_flat': 'in_playlist',
            'dump_single_json': True,
            'quiet': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(query)
            a = [entry['url'] for entry in playlist_info['entries']]
            return a
            