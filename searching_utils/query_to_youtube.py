import ytmusicapi
from yt_dlp import YoutubeDL

async def get_song_url(query: str) -> str:
    yt = ytmusicapi.YTMusic()
    try:
        results = yt.search(query)
        if results and "videoId" in results[0]:
            video_id = results[0]["videoId"]
            print("Song found using YouTube Music.")
            return f"https://music.youtube.com/watch?v={video_id}"
    except Exception:
        pass
    
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best"
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            search_results = ydl.extract_info(f"ytsearch:{query}", download=False)
            if search_results and "entries" in search_results and search_results["entries"]:
                first_result = search_results["entries"][0]
                if "id" in first_result:
                    print("Song found using YouTube.")
                    return f"https://www.youtube.com/watch?v={first_result['id']}"
        except Exception:
            pass
    
    raise Exception("There was an error getting the URL or no results were found.")
