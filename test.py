# import yt_dlp

# def check_source_supported(url):
#     ydl_opts = {
#         'quiet': True,
#         'skip_download': True,
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             result = ydl.extract_info(url=url)
#             site = result["extractor"]
#             return site
#         except Exception as e:
#             return None

# # Example usage
# url = 'https://www.youtube.com/watch?list=PL7DA3D097D6FDBC02'
# is_supported = check_source_supported(url)

# if is_supported:
#     print(f"Source is {is_supported} and supported by yt-dlp.")
# else:
#     print("Source is not supported by yt-dlp.")


from urllib.parse import urlparse


