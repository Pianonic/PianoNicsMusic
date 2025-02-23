from spotdl import Spotdl
from spotdl.utils.spotify import SpotifyError
import os

# Global variable to track initialization state
spotify_instance = None

async def initialize_spotify_client(spotify_credentials_provided: bool):
    global spotify_instance

    if not spotify_credentials_provided:
        return

    if spotify_instance is not None:
        raise RuntimeError("Spotify client is already initialized.")

    try:
        spotify_instance = Spotdl(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
        )
    except SpotifyError as e:
        raise RuntimeError(f"Failed to initialize Spotify client: {e}")

async def get_spotify_client() -> Spotdl:
    global spotify_instance

    if spotify_instance is None:
        raise RuntimeError("Spotify client has not been initialized. Call 'initialize_spotify_client' first.")
    
    return spotify_instance
