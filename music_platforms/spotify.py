import os
from spotdl import Spotdl
from dotenv import load_dotenv
import yt_dlp as youtube_dl
from models.music_information import MusicInformation

load_dotenv()
spotdl = Spotdl(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))

async def get_streaming_url(spotify_url):    
    song = spotdl.search([spotify_url])
    youtube_url = spotdl.get_download_urls(song)[0]

    ydl_opts = {
        'format': 'bestaudio/best',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        track_link = info_dict.get('url', '')
        track_name = info_dict.get('title', '')
        track_author = info_dict.get('uploader', '')
        image = info_dict.get('thumbnail', '')

    # Print the extracted data
    # print("Link:", track_link)
    # print("Title:", track_name)
    # print("Author:", track_author)
    # print("Image:", image)

    return MusicInformation(streaming_url=track_link, song_name=track_name, author=track_author, image_url=image)