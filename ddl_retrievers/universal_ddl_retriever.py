import yt_dlp
from models.music_information import MusicInformation

async def get_streaming_url(url) -> MusicInformation:
    
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

        # Get the best audio URL
        if 'url' in info_dict:
            track_link = info_dict['url']
        else:
            # Find the audio format with the highest bitrate
            formats = info_dict.get('formats', [])
            audio_formats = [f for f in formats if f.get('acodec') != 'none']
            if audio_formats:
                best_audio = max(audio_formats, key=lambda f: f.get('abr', 0) or 0)
                track_link = best_audio['url']
            else:
                track_link = formats[0]['url'] if formats else None
        track_name = info_dict['title']
        track_author = info_dict['uploader']
        try:
            thumbnails = info_dict['thumbnails']
            square_thumbnails = [thumb for thumb in thumbnails if 'width' in thumb and 'height' in thumb and thumb['width'] == thumb['height']]
            largest_square = max(square_thumbnails, key=lambda t: t['width'])
            thumbnail_url = largest_square['url']
        except:
            thumbnail_url = info_dict['thumbnail']

    return MusicInformation(streaming_url=track_link, song_name=track_name, author=track_author, image_url=thumbnail_url)
