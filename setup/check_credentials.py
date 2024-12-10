import os
from exceptions.discord_exceptions import InvalidDiscordTokenError
from exceptions.spotify_exceptions import InvalidSpotifyCredentialsError

async def check_spotify_credentials():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if client_id and client_secret:
        print("Spotify credentials have been successfully provided.")
    elif client_id or client_secret:
        raise InvalidSpotifyCredentialsError(
            "Both Spotify Client ID and Client Secret are required. "
            "Please ensure both credentials are provided correctly. "
            "If you don't have credentials, the bot will still be able to play Spotify tracks without them."
        )
    else:
        print("No Spotify credentials detected. The bot will still function and play Spotify tracks without them.")

def check_discord_credentials():
    discord_token = os.getenv('DISCORD_TOKEN')

    if discord_token:
        print("Discord token has been successfully provided.")
    else:
        raise InvalidDiscordTokenError("No Discord token detected. Please ensure the token is set correctly.")