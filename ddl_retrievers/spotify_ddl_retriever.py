import os
from dotenv import load_dotenv
from spotdl import Spotdl
import yt_dlp as youtube_dl
from ddl_retrievers import universal_ddl_retriever
from models.music_information import MusicInformation

load_dotenv()

spotdl = Spotdl(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))

async def get_streaming_url(spotify_url) -> MusicInformation:    
    song = spotdl.search([spotify_url])
    youtube_url = spotdl.get_download_urls(song)[0]

    return await universal_ddl_retriever.get_streaming_url(youtube_url)