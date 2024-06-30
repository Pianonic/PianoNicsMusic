import yt_dlp

class Data:
    def __init__(self, link, song_name, author, image):
        self.link = link
        self.song_name = song_name
        self.author = author
        self.image = image

async def GetYTLink(url):
    
    ydl_opts = {
        'format': 'bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)

    track_link = info_dict['url']
    track_name = info_dict['title']
    track_author = info_dict['uploader']
    image = info_dict['thumbnail']

    print("Link:", track_link)
    print("Title:", track_name)
    print("Author:", track_author)
    print("Image:", image)

    return Data(link=track_link, song_name=track_name, author=track_author, image=image)
