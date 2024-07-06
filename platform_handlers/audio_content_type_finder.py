import os
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from enums.audio_content_type import AudioContentType
from enums.platform import Platform
# from dotenv import load_dotenv

# load_dotenv()


from urllib.parse import urlparse
from urllib.parse import parse_qs

async def get_audio_content_type(query_url: str, platform: Platform) -> AudioContentType:
    if platform is Platform.YOUTUBE:
        parse_result = urlparse(query_url)
        query_params = parse_qs(parse_result.query)
        result = query_params.get("list", [None])[0]

        if result:
            if result.startswith('RD'):
                return AudioContentType.RADIO
            else:
                return AudioContentType.PLAYLIST
        else:
            return AudioContentType.SINGLE_SONG
    
    elif platform is Platform.SOUND_CLOUD:
        parse_result = urlparse(query_url)
        path = parse_result.path
        path_segments = path.strip("/").split("/")

        if "sets" in path_segments:
            return AudioContentType.PLAYLIST
        else:
            return AudioContentType.SINGLE_SONG

        # track_links = []
        # if "/sets/" in url:
        #     ydl_opts = {
        #         'flat_playlist': True,
        #         'dump_single_json': True,
        #         'quiet': True
        #     }

        #     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        #         info_dict = ydl.extract_info(url, download=False)
        #         for video in info_dict['entries']:
        #             track_links.append(video['webpage_url'])
        #     return track_links
        # else:
        #     return [url]
    
    elif platform is Platform.SPOTIFY:

        parse_result = urlparse(query_url)
        path = parse_result.path
        path_segments = path.strip("/").split("/")

        if "playlist" in path_segments:
            return AudioContentType.PLAYLIST
        elif "album" in path_segments:
            return AudioContentType.ALBUM
        elif "track" in path_segments:
            return AudioContentType.SINGLE_SONG
        else:
            return AudioContentType.NOT_SUPPORTED

    elif platform is Platform.NO_URL:
        return AudioContentType.QUERY
        # track_links = []
        # if "/playlist/" in url:
            
        #     client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
        #     sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        #     playlist_id = url.split('/')[-1].split('?')[0]
        #     playlist = sp.playlist(playlist_id)

        #     for item in playlist['tracks']['items']:
        #         track = item['track']
        #         track_links.append(track['external_urls']['spotify'])
        # else:
        #     track_links.append(url)
        # return track_links
    else:
        # IMPLEMENT HERE A CHECKER IF THE VIDEO IS INSTANTLY PLAYABLE IF NOT
        # MAKE WITH YOUTUBE_DLP TO CHECK IF IT IS A YTDLP SOURCE AND IF YES CHECK IF IT IS A PLAYLIST.
        return AudioContentType.SINGLE_SONG