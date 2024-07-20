from typing import List
from urllib.parse import urlparse
from models.queue_object import QueueObject
from platform_handlers.audio_content_type_finder import get_audio_content_type
from platform_handlers.music_platform_finder import find_platform
from enums.audio_content_type import AudioContentType
from enums.platform import Platform
import yt_dlp
import ytmusicapi

from spotipy import SpotifyClientCredentials
import spotipy
import os

async def get_streaming_url(query_url: str):
    platform = await find_platform(query_url)
    audio_content_type = get_audio_content_type(query_url, platform)
    return "a" 

async def get_urls(query: str) -> List[QueueObject]:
    platform = await find_platform(query)
    audio_content_type = await get_audio_content_type(query, platform)

    if audio_content_type is AudioContentType.NOT_SUPPORTED:
        return [QueueObject()]
    
    elif audio_content_type is AudioContentType.QUERY:
        yt = ytmusicapi.YTMusic()
        video_id = yt.search(query)[0]["videoId"]
        yt_music_url = f"https://music.youtube.com/watch?v={video_id}"
        return [QueueObject(yt_music_url, False)]
    
    elif audio_content_type is AudioContentType.SINGLE_SONG:
        return [QueueObject(query, False)]
    
    elif (audio_content_type is AudioContentType.PLAYLIST or audio_content_type is AudioContentType.ALBUM) and platform is Platform.SPOTIFY:
        client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        parse_result = urlparse(query)
        path = parse_result.path
        path_segments = path.strip("/").split("/")
        playlist_or_album_id = path_segments[-1]

        track_links = List[QueueObject]

        if audio_content_type is AudioContentType.PLAYLIST:
            playlist_or_album = sp.playlist(playlist_or_album_id)
            track_links = [QueueObject(item['track']['external_urls']['spotify'], False) for item in playlist_or_album['tracks']['items']]


        elif audio_content_type is AudioContentType.ALBUM:
            playlist_or_album = sp.album(playlist_or_album_id)
            track_links = [QueueObject(item['external_urls']['spotify'], False) for item in playlist_or_album['tracks']['items']]

        else:
            print("error")

        return track_links


    elif (audio_content_type is AudioContentType.PLAYLIST or audio_content_type is AudioContentType.RADIO) and platform != Platform.SPOTIFY:
        ydl_opts = {
            'extract_flat': 'in_playlist',
            'dump_single_json': True,
            'quiet': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(query)
            queue_object_list = [QueueObject(entry['url'], False) for entry in playlist_info['entries']]
            return queue_object_list
        
    else:
        print("skipped")
            