import logging
import discord
from discord.ext import commands
from discord_utils import embed_generator

logger = logging.getLogger('PianoNicsMusicBot')

class Skip(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['next', 'advance', 'skip_song', 'move_on', 'play_next'])
    async def skip(self, ctx):
        try:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

            if voice_client:
                voice_client.stop()
            
                if ctx.message:
                    await ctx.message.add_reaction("⏭️")
                else:
                    await ctx.respond(embed=await embed_generator.create_success_embed("⏭️ Skipped", "Skipped Song"))
            else:
                if ctx.message:
                    await ctx.send(embed=await embed_generator.create_error_embed("Error", "Bot is not connected to a Voice channel"))
                else:
                    await ctx.respond(embed=await embed_generator.create_error_embed("Error", "Bot is not connected to a Voice channel"))
        except Exception as e:
            logger.error(f"Error in skip command: {e}")
            try:
                if ctx.message:
                    await ctx.send(embed=await embed_generator.create_error_embed("Error", "An error occurred while skipping"))
                else:
                    await ctx.respond(embed=await embed_generator.create_error_embed("Error", "An error occurred while skipping"))
            except Exception as send_error:
                logger.error(f"Failed to send error message: {send_error}")