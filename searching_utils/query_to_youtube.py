import ytmusicapi
from yt_dlp import YoutubeDL

def get_url(query: str) -> str:
    yt = ytmusicapi.YTMusic()
    results = yt.search(query)

    if results:
        video_id = results[0]["videoId"]
        return f"https://music.youtube.com/watch?v={video_id}"
    else:
        with YoutubeDL({"quiet": True}) as ydl:
            search_results = ydl.extract_info(f"ytsearch:{query}", download=False)
            if "entries" in search_results and search_results["entries"]:
                first_result = search_results["entries"][0]
                return f"https://www.youtube.com/watch?v={first_result['id']}"
            
    raise Exception("There was an error getting the url")