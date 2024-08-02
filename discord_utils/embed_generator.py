import discord

async def create_embed(title, contents, image=None):
    if all(isinstance(item, str) for item in contents):
        embed=discord.Embed(title=title, color=0x282841)
        if(image):
            embed.set_thumbnail(url=image)
            
        embed.add_field(name="", value=contents, inline=False)
        
        embed.set_footer(text="PianoNics-Music, created by the one and only PianoNic")
        return embed
    else:
        embed=discord.Embed(title=title, color=0x282841)
        
        for content in contents:
            embed.add_field(name=content.author, value=content.link, inline=False)
        embed.set_footer(text="PianoNics-Music, created by the one and only PianoNic")
        return embed