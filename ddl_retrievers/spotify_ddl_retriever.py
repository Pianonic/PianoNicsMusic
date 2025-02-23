import time
from spotdl import Spotdl
import yt_dlp as youtube_dl
from models.music_information import MusicInformation
import searching_utils.spotify_to_youtube as STY

async def get_streaming_url(spotify_url: str) -> MusicInformation:    
    start_time = time.time()
    
    print("Start get url")
    youtube_url = await STY.get_song_url(spotify_url)
    elapsed_time = time.time() - start_time
    print(f"Completed get url in {elapsed_time:.2f} seconds")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }
    
    start_time = time.time()
    print("Start get ddl")
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        track_link = info_dict.get('url', '')
        track_name = info_dict.get('title', '')
        track_author = info_dict.get('uploader', '')
        
        try:
            thumbnails = info_dict.get('thumbnails', [])
            square_thumbnails = [thumb for thumb in thumbnails if 'width' in thumb and 'height' in thumb and thumb['width'] == thumb['height']]
            largest_square = max(square_thumbnails, key=lambda t: t['width'])
            thumbnail_url = largest_square['url']
        except:
            thumbnail_url = info_dict.get('thumbnail', '')

    elapsed_time = time.time() - start_time
    print(f"Completed get ddl in {elapsed_time:.2f} seconds")
    
    start_time = time.time()
    print("Start finalization")
    result = MusicInformation(streaming_url=track_link, song_name=track_name, author=track_author, image_url=thumbnail_url)
    elapsed_time = time.time() - start_time
    print(f"Completed finalization in {elapsed_time:.2f} seconds")
    
    print("Finished")
    return result