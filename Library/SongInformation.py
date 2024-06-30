import os
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

def get_song_info(url):
    if "www.youtube.com" in url or "youtu.be" in url:
        if "&list=" in url:
            playlist_id = url.split("&list=")[1]
            if playlist_id.startswith('RD'):
                print("Radio playlists are not supported.")
                return []
            ydl_opts = {
                'extract_flat': 'in_playlist',
                'dump_single_json': True,
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_id, download=False)
                playlist_urls = [entry['url'] for entry in playlist_info['entries']]

            return playlist_urls
        else:
            return [url]
    
    if "https://soundcloud.com" in url:
        track_links = []
        if "/sets/" in url:
            ydl_opts = {
                'flat_playlist': True,
                'dump_single_json': True,
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                for video in info_dict['entries']:
                    track_links.append(video['webpage_url'])
            return track_links
        else:
            return [url]
    
    if "https://open.spotify.com" in url:
        track_links = []
        if "/playlist/" in url:
            
            client_credentials_manager = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'))
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

            playlist_id = url.split('/')[-1].split('?')[0]
            playlist = sp.playlist(playlist_id)

            for item in playlist['tracks']['items']:
                track = item['track']
                track_links.append(track['external_urls']['spotify'])
        else:
            track_links.append(url)
        return track_links
    
    return [url]

#print(get_song_info("https://open.spotify.com/playlist/1CQQVPBBlpP03GkEVjyd33"))