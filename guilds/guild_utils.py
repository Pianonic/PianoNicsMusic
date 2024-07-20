import discord
from models.guild_music_information import GuildMusicInformation

guilds_info = []

async def get_guild_music_information(guild_id: int) -> GuildMusicInformation | None:
    global guilds_info

    for guild in guilds_info:
        if guild.id == guild_id:
            return guild
    return None

async def delete_guild(guild_id):
    global guilds_info

    for index, guild in enumerate(guilds_info):
        if guild.id == guild_id:
            guilds_info.pop(index)
            break
        
async def create_new_guild_music_information_and_join(guild_id: int, voice_channel: discord.VoiceChannel) -> GuildMusicInformation:
    global guilds_info

    voice_client = await voice_channel.connect()

    new_guild = GuildMusicInformation(id=guild_id, voice_channel=voice_channel, voice_client=voice_client, is_bot_busy=False, queue=[], loop_queue=False)
    guilds_info.append(new_guild)
    return new_guild