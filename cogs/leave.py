import logging
import discord
from discord.ext import commands
from db_utils import db_utils
from discord_utils import embed_generator

logger = logging.getLogger('PianoNicsMusicBot')

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['exit', 'quit', 'bye', 'farewell', 'goodbye', 'leave_now', 'disconnect', 'stop_playing'])
    async def leave(ctx):
        try:
            voice_client = ctx.voice_client
            user_channel = ctx.author.voice.channel if ctx.author.voice else None
            bot_channel = voice_client.channel if voice_client else None

            if voice_client and bot_channel:
                if not user_channel or user_channel.id != bot_channel.id:
                    if ctx.message:
                        await ctx.send(embed=await embed_generator.create_error_embed("Access Denied", f"Only users in `{bot_channel.name}` can disconnect the bot. Please join that channel to use this command."))
                    else:
                        await ctx.respond(embed=await embed_generator.create_error_embed("Access Denied", f"Only users in `{bot_channel.name}` can disconnect the bot. Please join that channel to use this command."))
                    return

            if voice_client:
                try:
                    await db_utils.delete_queue(ctx.guild.id)
                except Exception as e:
                    logger.error(f"Error deleting queue: {e}")
                
                try:
                    voice_client.stop()
                except Exception as e:
                    logger.error(f"Error stopping voice client: {e}")
                
                try:
                    await voice_client.disconnect()
                except Exception as e:
                    logger.error(f"Error disconnecting voice client: {e}")
            
                if ctx.message:
                    await ctx.message.add_reaction("👋")
                else:
                    await ctx.respond(embed=await embed_generator.create_success_embed("👋 Goodbye", "Left the channel"))
            else:
                if ctx.message:
                    await ctx.send(embed=await embed_generator.create_error_embed("Error", "Bot is not connected to a Voice channel"))
                else:
                    await ctx.respond(embed=await embed_generator.create_error_embed("Error", "Bot is not connected to a Voice channel"))
        except Exception as e:
            logger.error(f"Error in leave command: {e}")
            try:
                if ctx.message:
                    await ctx.send(embed=await embed_generator.create_error_embed("Error", "An error occurred while leaving"))
                else:
                    await ctx.respond(embed=await embed_generator.create_error_embed("Error", "An error occurred while leaving"))
            except Exception as send_error:
                logger.error(f"Failed to send error message: {send_error}")