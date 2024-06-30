import os
from spotdl import Spotdl
from dotenv import load_dotenv
import yt_dlp as youtube_dl

load_dotenv()
spotdl = Spotdl(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))

class Data:
    def __init__(self, link, song_name, author, image):
        self.link = link
        self.song_name = song_name
        self.author = author
        self.image = image

async def GetSFLinkRequest(spotify_url):
    # Initialize Spotify client
    

    # Get song metadata from Spotify URL
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
    print("Link:", track_link)
    print("Title:", track_name)
    print("Author:", track_author)
    print("Image:", image)

    # Create a Data object with the extracted data
    return Data(link=track_link, song_name=track_name, author=track_author, image=image)

# Example usage
# spotify_song_url = 'https://open.spotify.com/track/4uLU6hMCjMI75M1A2tKUQC'
# song_data = GetSFLinkRequest(spotify_song_url)
