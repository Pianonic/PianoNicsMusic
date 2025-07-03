import asyncio
import discord

from discord_utils import embed_generator
from platform_handlers import music_url_getter
from ddl_retrievers.universal_ddl_retriever import YouTubeError

async def play(ctx: discord.ApplicationContext, queue_url: str):
    loading_message = None
    try:
        try:
            loading_message = await ctx.respond(embed=await embed_generator.create_embed("Please Wait", "Searching song..."))
        except:
            loading_message = await ctx.send(embed=await embed_generator.create_embed("Please Wait", "Searching song..."))

        try:
            music_information = await music_url_getter.get_streaming_url(queue_url)
        except YouTubeError as e:
            # Handle YouTube-specific errors with user-friendly messages
            print(f"YouTube error for {queue_url}: {e}")
            if loading_message:
                await loading_message.edit(embed=await embed_generator.create_embed("⚠️ Video Error", str(e)))
            raise YouTubeError(str(e))  # Keep as YouTubeError to preserve error type
        except Exception as e:
            print(f"Error getting streaming URL for {queue_url}: {e}")
            if loading_message:
                await loading_message.edit(embed=await embed_generator.create_embed("Error", "Failed to get song information. Skipping..."))
            raise Exception(f"Failed to get streaming URL: {e}")

        try:
            await loading_message.edit(embed=await embed_generator.create_embed("Now Playing", f"**{music_information.song_name}**\nBy **{music_information.author}**", music_information.image_url))
        except Exception as e:
            print(f"Error updating loading message: {e}")
        
        voice_client: discord.VoiceClient = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        
        if not voice_client:
            print("No voice client found")
            raise Exception("Bot is not connected to a voice channel")
        
        try:
            # Use FFmpeg audio normalization filters
            audio_source = discord.FFmpegPCMAudio(
                music_information.streaming_url, 
                options='-vn -filter:a loudnorm=I=-25:TP=-1.5:LRA=11', 
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            )
              # Stop any currently playing audio before starting new playback
            if voice_client.is_playing():
                voice_client.stop()

            voice_client.play(audio_source)
        except Exception as e:
            print(f"Error starting playback: {e}")
            raise Exception(f"Failed to start audio playback: {e}")
        # Wait for playback to finish
        while voice_client.is_playing() or voice_client.is_paused():
            await asyncio.sleep(1)
                
    except YouTubeError as e:
        # Don't overwrite the specific YouTube error message that was already set
        print(f"Error in play function: {e}")
        raise e  # Re-raise the exception so the main loop can handle it
    except Exception as e:
        print(f"Error in play function: {e}")
        if loading_message:
            try:
                await loading_message.edit(embed=await embed_generator.create_embed("Error", "An error occurred while playing this song."))
            except:
                pass  # Ignore message edit errors
        raise e  # Re-raise the exception so the main loop can handle it