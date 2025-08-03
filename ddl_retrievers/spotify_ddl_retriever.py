import os
from dotenv import load_dotenv
from spotdl import Spotdl
import yt_dlp as youtube_dl
from ddl_retrievers import universal_ddl_retriever
from models.music_information import MusicInformation
import ytmusicapi
import logging

logger = logging.getLogger('PianoNicsMusic')

load_dotenv()

spotdl = Spotdl(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))

async def get_streaming_url(spotify_url) -> MusicInformation:    
    try:
        # Try Spotify first
        song = spotdl.search([spotify_url])
        if not song:
            raise Exception("No songs found from Spotify search")
        
        download_urls = spotdl.get_download_urls(song)
        if not download_urls:
            raise Exception("No download URLs found from Spotify")
        
        youtube_url = download_urls[0]
        return await universal_ddl_retriever.get_streaming_url(youtube_url)
        
    except Exception as spotify_error:
        logger.error(f"Spotify search failed: {spotify_error}")
        
        # Extract song information for YouTube Music search
        try:
            song_info = spotdl.search([spotify_url])
            if song_info and len(song_info) > 0:
                song_name = song_info[0].name
                artist_name = song_info[0].artist
                search_query = f"{artist_name} - {song_name}"
            else:
                # If we can't get song info, extract from URL
                url_parts = spotify_url.split('/')
                track_id = url_parts[-1].split('?')[0]
                search_query = f"spotify track {track_id}"
        except Exception:
            search_query = spotify_url
        
        # Try YouTube Music as fallback
        try:
            logger.info(f"Trying YouTube Music search for: {search_query}")
            yt = ytmusicapi.YTMusic()
            search_results = yt.search(search_query, filter="songs")
            if search_results and len(search_results) > 0:
                video_id = search_results[0]["videoId"]
                yt_music_url = f"https://music.youtube.com/watch?v={video_id}"
                return await universal_ddl_retriever.get_streaming_url(yt_music_url)
            else:
                raise Exception("No results found on YouTube Music")
                
        except Exception as ytmusic_error:
            logger.error(f"YouTube Music search failed: {ytmusic_error}")
            raise Exception(f"Both Spotify and YouTube Music failed. Spotify error: {spotify_error}")