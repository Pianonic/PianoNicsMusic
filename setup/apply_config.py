import configparser
from discord import Bot

async def apply_config(bot: Bot):
    config = configparser.ConfigParser()
    config.read('config.ini')

    ask_in_dms = config.getboolean('Bot', 'AskInDMs', fallback=False)
    admin_userid = config.getint('Admin', 'UserID', fallback=0)
    
    if ask_in_dms and admin_userid:
        user = await bot.fetch_user(admin_userid)
        
        dm_channel = await user.create_dm()
        
        messages = await dm_channel.history().flatten()
        
        for msg in messages:
            try:
                await msg.delete()
            except Exception as e:
                print(f"Skipped message due to error: {str(e)}")

        await user.send(f"Bot is ready and logged in as {bot.user.name}")