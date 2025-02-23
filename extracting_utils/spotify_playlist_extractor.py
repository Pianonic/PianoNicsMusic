import os
from typing import List
from urllib.parse import urlparse
from spotipy import SpotifyClientCredentials
import spotipy
import music_utils.audio_content_type_finder as ACTF
from enums.audio_content_type import AudioContentType
from spotapi import PublicPlaylist

async def get_song_urls(spotify_url: str) -> List[str]:
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if client_id and client_secret:
        return await get_song_urls_with_credentials(spotify_url, client_id, client_secret)
    elif client_id or client_secret:
        raise Exception("Both Spotify client ID and client secret are required.")
    else:
        return await get_song_urls_without_credentials(spotify_url)
    

async def get_song_urls_without_credentials(spotify_url: str) -> List[str]:
    audio_content_type: AudioContentType = await ACTF.get_audio_content_type(spotify_url)

    public_playlist = PublicPlaylist(spotify_url)
    playlist_tracks = List(public_playlist.paginate_playlist())
    playlist_metadata = public_playlist.get_playlist_info(limit=0)
    playlist_name = public_playlist.name if hasattr(public_playlist, 'name') else "Unnamed_Playlist"
    playlist_safe_name = playlist_metadata['data']['playlistV2']['name']
    playlist_entries: List[str]

    for page in playlist_tracks:
        for item in page.get("items", []):
            track = item.get("itemV2", {}).get("data", {})
            track_name = track.get("name")
            if track_name:
                # Attempt to decode using utf-8, ignoring errors if they occur
                track_name = track_name.encode('utf-8', 'ignore').decode('utf-8')
            artists = track.get("artists", {}).get("items", [])
            artist_names = [artist.get("profile", {}).get("name") for artist in artists if artist.get("profile", {}).get("name")]
            if track_name and artist_names:
                playlist_entries.append(f"{track_name} by {artist_names}")
    if len(playlist_entries) > 0:
        return playlist_entries
    else:
        raise Exception("No valid tracks found in the playlist or failed to fetch data.")

async def get_song_urls_with_credentials(spotify_url: str, client_id: str, client_secret: str) -> List[str]:
    audio_content_type: AudioContentType = await ACTF.get_audio_content_type(spotify_url)

    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    parse_result = urlparse(spotify_url)
    path = parse_result.path
    path_segments = path.strip("/").split("/")
    playlist_or_album_id = path_segments[-1]

    if audio_content_type is AudioContentType.PLAYLIST:
        playlist_or_album = sp.playlist(playlist_or_album_id)
        return [item['track']['external_urls']['spotify'] for item in playlist_or_album['tracks']['items']]

    elif audio_content_type is AudioContentType.ALBUM:
        playlist_or_album = sp.album(playlist_or_album_id)
        return [item['external_urls']['spotify'] for item in playlist_or_album['tracks']['items']]
    
    else:
        raise NotImplementedError("This type of Spotify content is not implemented.")