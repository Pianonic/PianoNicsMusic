import yt_dlp as youtube_dl

class Data:
    def __init__(self, link, song_name, author, image):
        self.link = link
        self.song_name = song_name
        self.author = author
        self.image = image

async def GetSCLink(DownloadLink):
    ydl_opts = {
        'format': 'bestaudio/best',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(DownloadLink, download=False)
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
# soundcloud_url = 'https://soundcloud.com/audiobe/snowfall-super-slowed-reverb'
# data = GetSCLink(soundcloud_url)
