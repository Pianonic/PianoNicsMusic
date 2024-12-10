import asyncio
import discord

from discord_utils import embed_generator
from platform_handlers import music_url_getter

async def play(ctx: discord.ApplicationContext, queue_url: str):
    loading_embed = await embed_generator.create_embed("Please Wait", "Searching song...")

    try:
        loading_message = await ctx.respond(embed=loading_embed)
    except:
        loading_message = await ctx.send(embed=loading_embed)

    music_information = await music_url_getter.get_streaming_url(queue_url)

    await loading_message.edit(embed=await embed_generator.create_embed("Now Playing", f"**{music_information.song_name}**\nBy **{music_information.author}**", music_information.image_url ))
    
    # Create an audio source and player
    audio_source = discord.FFmpegPCMAudio(music_information.streaming_url, options='-vn', before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
    player = discord.PCMVolumeTransformer(audio_source)
    
    voice_client: discord.VoiceChannel = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    
    voice_client.play(player)

    while voice_client.is_playing() or voice_client.is_paused():
        await asyncio.sleep(1) 