import os
from dotenv import load_dotenv
from spotdl import Spotdl
import yt_dlp as youtube_dl
from models.music_information import MusicInformation

load_dotenv()

spotdl = Spotdl(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))

async def get_streaming_url(spotify_url) -> MusicInformation:    
    song = spotdl.search([spotify_url])
    youtube_url = spotdl.get_download_urls(song)[0]

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        track_link = info_dict.get('url', '')
        track_name = info_dict.get('title', '')
        track_author = info_dict.get('uploader', '')

        try:
            thumbnails = info_dict.get('thumbnails', [])
            square_thumbnails = [thumb for thumb in thumbnails if 'width' in thumb and 'height' in thumb and thumb['width'] == thumb['height']]
            largest_square = max(square_thumbnails, key=lambda t: t['width'])
            thumbnail_url = largest_square['url']
        except:
            thumbnail_url = info_dict.get('thumbnail', '')

    return MusicInformation(streaming_url=track_link, song_name=track_name, author=track_author, image_url=thumbnail_url)