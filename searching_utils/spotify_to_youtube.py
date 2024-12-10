import os
from bs4 import BeautifulSoup
import requests
from spotdl import Spotdl
from exceptions.spotify_exceptions import MissingSpotifyCredentialsError
from searching_utils.query_to_youtube import get_url

def get_url(spotify_url: str) -> str:
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if client_id and client_secret:
        return get_url_with_credentials(spotify_url, client_id, client_secret)
    elif client_id or client_secret:
        raise MissingSpotifyCredentialsError("Both client ID and client secret are required.")
    else:
        return get_url_without_credentials(spotify_url)

def get_url_without_credentials(spotify_url: str) -> str:
    response = requests.get(spotify_url)
    
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    
    meta_tag = soup.find('meta', {'property': 'og:description'})
    
    if not meta_tag or 'content' not in meta_tag.attrs:
        raise ValueError("Could not find the 'og:description' meta tag")

    search_query = meta_tag['content']

    return get_url(search_query)

def get_url_with_credentials(spotify_url: str, client_id: str, client_secret: str) -> str:
    spotdl = Spotdl(client_id=client_id, client_secret=client_secret)
    song = spotdl.search([spotify_url])
    return spotdl.get_download_urls(song)[0]