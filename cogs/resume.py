import logging
import discord
from discord.ext import commands
from discord_utils import embed_generator

logger = logging.getLogger('PianoNicsMusicBot')

class Resume(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['continue', 'unpause', 'proceed', 'restart', 'go', 'resume_playback'])
    async def resume(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client and hasattr(voice_client, 'resume'):
            voice_client.resume()  # type: ignore
        
            if ctx.message:
                await ctx.message.add_reaction("▶️")
            else:
                await ctx.respond(embed=await embed_generator.create_success_embed("▶️ Resumed", "Resumed the music"))

        else:
            if ctx.message:
                await ctx.send(embed=await embed_generator.create_error_embed("Error", "Bot is not connected to a Voice channel"))
            else:
                await ctx.respond(embed=await embed_generator.create_error_embed("Error", "Bot is not connected to a Voice channel"))