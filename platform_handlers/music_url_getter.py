from typing import List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests
import ddl_retrievers.spotify_ddl_retriever
import ddl_retrievers.tiktok_ddl_retriever
import ddl_retrievers.universal_ddl_retriever
from models.music_information import MusicInformation
import ddl_retrievers
from platform_handlers.audio_content_type_finder import get_audio_content_type
from platform_handlers.music_platform_finder import find_platform
from enums.audio_content_type import AudioContentType
from enums.platform import Platform
import yt_dlp
import ytmusicapi

from spotipy import SpotifyClientCredentials
import spotipy
import os

async def get_streaming_url(query_url: str) -> MusicInformation:
    platform = await find_platform(query_url)

    if platform is Platform.SPOTIFY:
        return await ddl_retrievers.spotify_ddl_retriever.get_streaming_url(query_url)

    elif platform is Platform.TIK_TOK:
        return await ddl_retrievers.tiktok_ddl_retriever.get_streaming_url(query_url)

    elif platform is Platform.SOUND_CLOUD:
        parsed_url = urlparse(query_url)

        subdomain = parsed_url.hostname.split('.')[0]

        if "api" in subdomain:
            response = requests.get(f"https://w.soundcloud.com/player/?url={query_url}")
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')

            canonical_link = soup.find('link', rel='canonical')
            href = canonical_link.get('href')

            return await ddl_retrievers.universal_ddl_retriever.get_streaming_url(href)
        
        else:
            return await ddl_retrievers.universal_ddl_retriever.get_streaming_url(query_url)


    elif platform is Platform.ANYTHING_ELSE:
        audio_content_type = await get_audio_content_type(query_url, platform)

        if audio_content_type is AudioContentType.YT_DLP:
            return await ddl_retrievers.universal_ddl_retriever.get_streaming_url(query_url)
        else:
            parsed_url = urlparse(query_url)
            song_name = os.path.basename(parsed_url.path)
            
            return MusicInformation(query_url, song_name, "unkown", 'https://i.giphy.com/LNOZoHMI16ydtQ8bGG.webp')
        
    else:
        return await ddl_retrievers.universal_ddl_retriever.get_streaming_url(query_url)

async def get_urls(query: str) -> List[str]:
    platform = await find_platform(query)
    audio_content_type = await get_audio_content_type(query, platform)

    if audio_content_type is AudioContentType.NOT_SUPPORTED:
        return []
    
    # TikTok
    elif audio_content_type is Platform.TIK_TOK:
        return [query]

    elif audio_content_type is AudioContentType.QUERY:
        yt = ytmusicapi.YTMusic()
        video_id = yt.search(query)[0]["videoId"]
        yt_music_url = f"https://music.youtube.com/watch?v={video_id}"
        return [yt_music_url]
    
    elif audio_content_type is AudioContentType.SINGLE_SONG:
        return [query]
    
    # Spotify
    elif (audio_content_type is AudioContentType.PLAYLIST or audio_content_type is AudioContentType.ALBUM) and platform is Platform.SPOTIFY:
        client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        parse_result = urlparse(query)
        path = parse_result.path
        path_segments = path.strip("/").split("/")
        playlist_or_album_id = path_segments[-1]

        if audio_content_type is AudioContentType.PLAYLIST:
            playlist_or_album = sp.playlist(playlist_or_album_id)
            return [item['track']['external_urls']['spotify'] for item in playlist_or_album['tracks']['items']]

        elif audio_content_type is AudioContentType.ALBUM:
            playlist_or_album = sp.album(playlist_or_album_id)
            return [item['external_urls']['spotify'] for item in playlist_or_album['tracks']['items']]

        else:
            raise NotImplementedError("This type of Spotify content is not implemented.")

    # Soundcloud and Youtube
    elif (audio_content_type is AudioContentType.PLAYLIST or audio_content_type is AudioContentType.RADIO) and platform != Platform.SPOTIFY:
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(query)
            return [entry['url'] for entry in playlist_info['entries']]

    # Anything else
    elif audio_content_type is AudioContentType.YT_DLP:
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(query)
            entries = playlist_info.get("entries", None)

            if entries:
                return [entry['url'] for entry in entries]
            else:
                return [query]    

    else:
        raise NotImplementedError("This type of Audio Content is not implemented.")
            