import discord

from utils import get_footer_text

async def create_embed(title, contents, image=None, embed_type="info"):
    colors = {
        "info": 0x282841,      # Default dark blue
        "success": 0x3ba55d,   # Muted green
        "error": 0xed4245,     # Muted red
        "warning": 0xfee75c    # Muted yellow
    }
    
    color = colors.get(embed_type, colors["info"])
    
    if isinstance(contents, str) or all(isinstance(item, str) for item in contents if isinstance(contents, list)):
        embed = discord.Embed(title=title, color=color)
        if image:
            embed.set_thumbnail(url=image)
            
        content_text = contents if isinstance(contents, str) else "\n".join(contents)
        embed.add_field(name="", value=content_text, inline=False)
        
        embed.set_footer(text=get_footer_text())
        return embed
    else:
        embed = discord.Embed(title=title, color=color)
        
        for content in contents:
            embed.add_field(name=content.author, value=content.link, inline=False)
        embed.set_footer(text=get_footer_text())
        return embed

async def create_success_embed(title, message):
    return await create_embed(title, message, embed_type="success")

async def create_error_embed(title, message):
    return await create_embed(title, message, embed_type="error")

async def create_info_embed(title, message):
    return await create_embed(title, message, embed_type="info")

async def create_warning_embed(title, message):
    return await create_embed(title, message, embed_type="warning")