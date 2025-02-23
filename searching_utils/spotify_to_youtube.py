import os
from bs4 import BeautifulSoup
import requests
from spotdl import Spotdl

from searching_utils import query_to_youtube as QTY
from setup.spotify_client_manager import get_spotify_client

async def get_song_url(spotify_url: str) -> str:
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if client_id and client_secret:
        return await get_song_url_with_credentials(spotify_url)
    elif client_id or client_secret:
        raise Exception("Both Spotify client ID and client secret are required.")
    else:
        return await get_song_url_without_credentials(spotify_url)

async def get_song_url_without_credentials(spotify_url: str) -> str:
    response = requests.get(spotify_url)
    
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    meta_tag = soup.find('meta', {'property': 'og:description'})
    
    if not meta_tag or 'content' not in meta_tag.attrs:
        raise Exception("Could not find the 'og:description' meta tag")

    search_query = meta_tag['content']

    return await QTY.get_song_url(search_query)

async def get_song_url_with_credentials(spotify_url: str) -> str:
    spotdl = await get_spotify_client()
    song = spotdl.search([spotify_url])
    return spotdl.get_download_urls(song)[0]