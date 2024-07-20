import discord
from discord.ext import commands

class Stop(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['halt', 'cease', 'end', 'terminate', 'shutdown', 'suspend'])
    async def stop(self, ctx):
        await self.stop_command(ctx)
        

    @discord.slash_command(name="stop", description="Stops the currently playing audio")
    async def stop_slash(self, ctx):
        await self.stop_command(ctx)


    async def stop_command(self, ctx):
        global guilds_info
        
        for guild in guilds_info:
            if guild.id == ctx.guild.id:
                current_guild = guild
                break

        if current_guild:
            current_guild.loop_queue = False
            current_guild.queue = []
            current_guild.voice_client.stop()
        
        if ctx.message:
            await ctx.message.add_reaction("⏹️")
        else:
            await ctx.respond("Stopped playing ⏹️")
