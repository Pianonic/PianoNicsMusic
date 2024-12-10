import configparser
import traceback

import discord

from db_utils import db_utils

async def handle_error(ctx, bot, error):
    traceback.print_exc()

    config = configparser.ConfigParser()
    config.read('config.ini')
    admin_userid = config.getint('Admin', 'UserID', fallback=0)

    if admin_userid:
        user = await bot.fetch_user(admin_userid)
        dm_channel = await user.create_dm()

        error_message = (
            f"An error occurred in the command '{ctx.command}':\n"
            f"Error: `{str(error)}`\n"
            f"Context: `{ctx}`\n"
            f"Traceback:\n```{traceback.format_exc()}```"
        )

        try:
            await dm_channel.send(error_message)
        except discord.Forbidden:
            print("Could not send DM to the admin user.")

    await rescue_bot(ctx)

async def rescue_bot(ctx):
    current_guild = await db_utils.get_guild(ctx.guild.id)
    voice_client: discord.VoiceClient | None = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if not voice_client and current_guild.last_connected_voice_id is not None:
        voice_channel = ctx.guild.get_channel(current_guild.last_connected_voice_id)
        
        if isinstance(voice_channel, discord.VoiceChannel):
            await voice_channel.connect()
            print("Bot was rescued from exception")