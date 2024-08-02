async def delete_queue(guild_id):
    guild = await get_guild_music_information(guild_id)
    guild.queue.clear()

async def delete_guild(guild_id):
    global guilds_info

    for index, guild in enumerate(guilds_info):
        if guild.id == guild_id:
            guilds_info.pop(index)
            break