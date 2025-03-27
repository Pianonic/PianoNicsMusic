import asyncio
import discord

from discord_utils import embed_generator
from platform_handlers import music_url_getter

async def play(ctx: discord.ApplicationContext, queue_url: str):
    try:
        loading_message = await ctx.respond(embed=await embed_generator.create_embed("Please Wait", "Searching song..."))
    except:
        loading_message = await ctx.send(embed=await embed_generator.create_embed("Please Wait", "Searching song..."))

    music_information = await music_url_getter.get_streaming_url(queue_url)

    await loading_message.edit(embed=await embed_generator.create_embed("Now Playing", f"**{music_information.song_name}**\nBy **{music_information.author}**", music_information.image_url ))
    
    # Use FFmpeg audio normalization filters
    audio_source = discord.FFmpegPCMAudio(
        music_information.streaming_url, 
        options='-vn -filter:a loudnorm=I=-25:TP=-1.5:LRA=11', 
        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    )
    
    voice_client: discord.VoiceChannel = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    
    # Stop any currently playing audio before starting new playback
    if voice_client.is_playing():
        voice_client.stop()

    voice_client.play(audio_source)

    while voice_client.is_playing() or voice_client.is_paused():
        await asyncio.sleep(1) 