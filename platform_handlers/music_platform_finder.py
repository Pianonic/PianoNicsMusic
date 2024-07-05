# import os
# from urllib.parse import urlparse
# from pytube import Search
# from music_platforms import spotify, tiktok
# from discord_utils import embed_generator
# from models.music_information import MusicInformation



# async def find_platformdd(ctx, query):
#     if ctx.message and ctx.message.attachments:
#         return await handle_attachment(ctx)
    
#     if not query:
#         await ctx.reply("⛔ No attachments or link provided.")
#         return
    
#     if "https://open.spotify.com" in query:
#         return await handle_platform(ctx, query, "Spotify")
    
#     if "https://vm.tiktok.com" in query or "https://www.tiktok.com" in query:
#         return await handle_platform(ctx, query, "TikTok")

#     if "https://" in query:
#         return await handle_url(ctx, query)

#     return await handle_search(ctx, query)

# async def handle_attachment(ctx):
#     message = await send_loading_message(ctx, "Attachment is loading...")
#     link = ctx.message.attachments[0].url
#     filename = os.path.basename(urlparse(link).path)
#     return ReturnData(MusicInformation(link=link, song_name=filename, author=ctx.author.mention, image="https://i.giphy.com/LNOZoHMI16ydtQ8bGG.webp"), message)

# async def handle_platform(ctx, query, platform):
#     platform_loading_times = {
#         "YouTube":  "YouTube is loading...",
#         "SoundCloud": "SoundCloud is loading...",
#         "Spotify": "Spotify is loading...",
#         "TikTok": "TikTok is loading..."
#     }
    
#     message_text = platform_loading_times.get(platform, f"{platform} is loading...")

#     message = await send_loading_message(ctx, message_text)

#     handler_functions = {
#         "YouTube": handle_youtube,
#         "SoundCloud": handle_soundcloud,
#         "Spotify": handle_spotify,
#         "TikTok": handle_tiktok
#     }
#     return await handler_functions[platform](ctx, query, message)

# async def send_loading_message(ctx, text):
#     try:
#         if ctx.message:
#             return await ctx.send(embed=embed_generator.CreateEmbed("⏳ Please Wait ⏳", text + " ⌚"))
#         else:
#             return await ctx.respond(embed=embed_generator.CreateEmbed("⏳ Please Wait ⏳", text + " ⌚"))
#     except:
#         return await ctx.send(embed=embed_generator.CreateEmbed("⏳ Please Wait ⏳", text + " ⌚"))

# async def handle_youtube(ctx, query, message):
#     return ReturnData(await youtube.get_streaming_url(query), message)

# async def handle_soundcloud(ctx, query, message):
#     return ReturnData(await soundcloud.get_streaming_url(query), message)

# async def handle_spotify(ctx, query, message):
#     return ReturnData(await spotify.get_streaming_url(query), message)

# async def handle_tiktok(ctx, query, message):
#     return ReturnData(await tiktok.get_streaming_url(query), message)

# async def handle_url(ctx, query):
#     message = await send_loading_message(ctx, "URL is loading...")
#     filename = os.path.basename(urlparse(query).path)
#     return ReturnData(MusicInformation(link=query, song_name=filename, author=ctx.author.mention, image="https://i.giphy.com/LNOZoHMI16ydtQ8bGG.webp"), message)

# async def handle_search(ctx, query):
#     message = await send_loading_message(ctx, "YouTube is loading...")
#     s = Search(query)
#     if not s.results:
#         await ctx.reply("⚠️ No search results found.")
#         return
#     video_url = s.results[0].watch_url
#     return ReturnData(await youtube.get_streaming_url(video_url), message)
