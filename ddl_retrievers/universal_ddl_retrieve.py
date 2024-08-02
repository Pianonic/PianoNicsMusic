import yt_dlp
from models.music_information import MusicInformation

async def get_streaming_url(url) -> MusicInformation:
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    track_link = info_dict['url']
    track_name = info_dict['title']
    track_author = info_dict['uploader']
    image = info_dict['thumbnail']

    return MusicInformation(streaming_url=track_link, song_name=track_name, author=track_author, image_url=image)
