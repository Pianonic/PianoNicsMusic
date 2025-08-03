import yt_dlp
from models.music_information import MusicInformation

class YouTubeError(Exception):
    """Custom exception for YouTube-specific errors"""
    pass

async def get_streaming_url(url) -> MusicInformation:
    
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
    }

    try:
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
    
    except yt_dlp.DownloadError as e:
        error_message = str(e)
        
        # Handle age-restricted content
        if "Sign in to confirm your age" in error_message or "inappropriate for some users" in error_message:
            raise YouTubeError("This video is age-restricted and cannot be played. Please try a different song.")
        
        # Handle private/unavailable videos
        elif "Private video" in error_message:
            raise YouTubeError("This video is private and cannot be played.")
        elif "Video unavailable" in error_message:
            raise YouTubeError("This video is unavailable.")
        elif "been removed" in error_message:
            raise YouTubeError("This video has been removed and is no longer available.")
        
        # Handle geo-blocking
        elif "not available in your country" in error_message:
            raise YouTubeError("This video is not available in your region.")
        
        # Handle live streams
        elif "live event" in error_message or "live stream" in error_message:
            raise YouTubeError("Live streams are not supported. Please try a regular video.")
        
        # Handle unviewable playlists (auto-generated topic playlists)
        elif "This playlist type is unviewable" in error_message:
            raise YouTubeError("This playlist type is unviewable. This often happens with auto-generated YouTube topic playlists. Please try a different playlist or individual songs.")
        
        # Generic yt-dlp error
        else:
            raise YouTubeError("Failed to process this video. It may be unavailable or restricted.")
    
    except Exception as e:
        # Handle any other unexpected errors
        raise YouTubeError(f"An unexpected error occurred: {str(e)}")
