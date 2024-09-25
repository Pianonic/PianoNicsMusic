# Standard library imports
import base64
import io
import json
import os

# Third-party imports
import discord
import websockets
from discord.commands import Option, OptionChoice
from discord.ext import commands
from dotenv import load_dotenv
import configparser

# Local application imports
from db_utils.db import setup_db
import db_utils.db_utils as db_utils
from discord_utils import embed_generator, player
from ai_server_utils import rvc_server_checker
from platform_handlers import music_url_getter
load_dotenv()

model_choices = []

# isServerRunning = rvc_server_pinger.check_connection()
# if(isServerRunning):
#     model_choices, index_choices = rvc_server_checker.fetch_choices()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=[".", "!", "$"], intents=intents, help_command=None)

@bot.event
async def on_ready():
    await setup_db()
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name="to da kuhle songs"))
    print(f"Bot is ready and logged in as {bot.user.name}")
    
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
            except:
                print("skiped message")

        await user.send(f"Bot is ready and logged in as {bot.user.name}")

@bot.command(aliases=['next', 'advance', 'skip_song', 'move_on', 'play_next'])
async def skip(ctx):
    voice_client: discord.VoiceClient | None = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client:
        voice_client.stop()
    
        if ctx.message:
            await ctx.message.add_reaction("⏭️")
        else:
            await ctx.respond("Skipped Song ⏭️")
    else:
        if ctx.message:
            await ctx.send("❗ Bot is not connected to a Voice channel")
        else:
            await ctx.respond("❗ Bot is not connected to a Voice channel")

@bot.command(aliases=['exit', 'quit', 'bye', 'farewell', 'goodbye', 'leave_now', 'disconnect', 'stop_playing'])
async def leave(ctx):
    voice_client: discord.VoiceClient | None = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client:
        await db_utils.delete_queue(ctx.guild.id)
        voice_client.stop()
    
        if ctx.message:
            await ctx.message.add_reaction("👋")
        else:
            await ctx.respond("Left the channel 👋")
    else:
        if ctx.message:
            await ctx.send("❗ Bot is not connected to a Voice channel")
        else:
            await ctx.respond("❗ Bot is not connected to a Voice channel")
    
@bot.command(aliases=['hold', 'freeze', 'break', 'wait', 'intermission'])
async def pause(ctx):
    voice_client: discord.VoiceClient | None = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        
    if voice_client:
        voice_client.pause()
    
        if ctx.message:
            await ctx.message.add_reaction("⏸️")
        else:
            await ctx.respond("Paued the music ⏸️")

    else:
        if ctx.message:
            await ctx.send("❗ Bot is not connected to a Voice channel")
        else:
            await ctx.respond("❗ Bot is not connected to a Voice channel")

@bot.command(aliases=['continue', 'unpause', 'proceed', 'restart', 'go', 'resume_playback'])
async def resume(ctx):
    voice_client: discord.VoiceClient | None = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client:
        voice_client.resume()
    
        if ctx.message:
            await ctx.message.add_reaction("▶️")
        else:
            await ctx.respond("Resumed the music ▶️")

    else:
        if ctx.message:
            await ctx.send("❗ Bot is not connected to a Voice channel")
        else:
            await ctx.respond("❗ Bot is not connected to a Voice channel")

# @bot.command(aliases=['lp', 'repeat', 'cycle', 'toggle_loop', 'toggle_repeat'])
# async def loop(ctx):
#     guild = await db_utils.get_guild(ctx.guild.id)

#     if not guild:
#         if ctx.message:
#             await ctx.send("❗ Bot is not connected to a Voice channel")
#         else:
#             await ctx.respond("❗ Bot is not connected to a Voice channel")
#         return
    
#     if guild.loop_queue:
#         if ctx.message:
#             await ctx.message.add_reaction("🔄")
#         else:
#             await ctx.respond("Now looping the queue 🔄")
#     else:
#         if ctx.message:
#             await ctx.message.add_reaction("⏹️")
#         else:
#             await ctx.respond("Stopped looping the queue ⏹️")

@bot.command(aliases=['fp', 'forceplay', 'playforce'])
async def force_play(ctx, *, query=None, insta_skip=False):
    guild = await db_utils.get_guild(ctx.guild.id)
    voice_client: discord.VoiceClient | None = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if not guild:
        if ctx.message:
            await ctx.send("❗ Bot is not connected to a Voice channel")
        else:
            await ctx.respond("❗ Bot is not connected to a Voice channel")
        return

    if (len(guild.queue) != 0) and voice_client:
        await db_utils.add_force_next_play_to_queue(ctx.guild.id, query)
    else:
        await ctx.send("No song is currently playing")
    
    if insta_skip:
        if ctx.message:
            await ctx.message.add_reaction("⏭️")
        else:
            await ctx.respond("Force playing Song ⏭️")

        voice_client.stop()
        
    else:
        if ctx.message:
            await ctx.message.add_reaction("📥")
        else:
            await ctx.respond("Playing next up 📥")

@bot.command()
async def shuffle(ctx):
    guild = await db_utils.get_guild(ctx.guild.id)

    if not guild:
        if ctx.message:
            await ctx.send("❗ Bot is not connected to a Voice channel")
        else:
            await ctx.respond("❗ Bot is not connected to a Voice channel")
        return

    await db_utils.shuffle_playlist(ctx.guild.id)

    if ctx.message:
        await ctx.message.add_reaction("🔀")
    else:
        await ctx.respond("Now Shuffeling 🔀")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    if ctx.message:
        await ctx.send(f'Pong! Latency is {latency}ms')
    else:
        await ctx.respond(f'Pong! Latency is {latency}ms')

@bot.command(aliases=['h', 'commands', 'command', 'cmds', 'cmd', 'info', 'information', 'assist', 'assistme', 'helpme', 'helppls', 'helpmepls', 'helpmeplease', 'helpmeout', 'helpmeoutpls', 'helpmeoutplease'])
async def help(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description="Here are all the available commands:",
        color=0x282841
    )

    commands_list = [
        #("stop", "Stops the currently playing audio"),
        ("skip", "Skips the currently playing audio"),
        ("leave", "Leaves the voice channel and stops playing audio"),
        ("loop", "Toggles looping of the queue"),
        ("ping", "Checks the bot's latency"),
        ("pause", "Pauses the currently playing audio"),
        ("resume", "Resumes the currently paused audio"),
        ("force_play", "Force plays the provided audio"),
        ("play", "Plays the provided audio"),
        ("play_with_ai_voice", "Plays the provided audio with custom AI voice")
    ]

    for name, description in commands_list:
        embed.add_field(name=f"/{name}", value=description, inline=False)

    embed.set_footer(text="PianoNics-Music, created by the one and only PianoNic")

    if ctx.message:
        await ctx.send(embed=embed)
    else:
        await ctx.respond(embed=embed)

@bot.command(name='play', aliases=['p', 'pl', 'play_song', 'queue', 'add', 'enqueue'])
async def play_command(ctx: discord.ApplicationContext, *, query=None):
    guild = await db_utils.get_guild(ctx.guild.id)

    song_urls = await music_url_getter.get_urls(query)
    await db_utils.add_to_queue(ctx.guild.id, song_urls)
    
    if guild:
        queue_length = len(song_urls)

        if queue_length > 1:
            if ctx.message:
                await ctx.send(embed=await embed_generator.create_embed("Queue", f"Added **{queue_length}** Songs to the Queue"))
            else:
                await ctx.respond(embed=await embed_generator.create_embed("Queue", f"Added **{queue_length}** Songs to the Queue"))

        else:
            if ctx.message:
                await ctx.message.add_reaction("📥")
            else:
                await ctx.respond("Added to the queue 📥")
        
        return
    else:
        await db_utils.create_new_guild(ctx.guild.id)
        await ctx.author.voice.channel.connect()
    
    while True:
        url = await db_utils.get_queue_entry(ctx.guild.id)

        if not url:
            break

        await player.play(ctx, url)   

    voice_client: discord.VoiceClient | None = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice_client:
        await voice_client.disconnect()
        
    await db_utils.delete_guild(ctx.guild.id)

###################################################
################# SLASH COMMANDS ##################
###################################################

@bot.slash_command(name="skip", description="Skips the currently playing audio")
async def skip_slash(ctx):
    await skip(ctx)

@bot.slash_command(name="leave", description="Leaves the voice channel and stops playing audio")
async def leave_slash(ctx):
    await leave(ctx)

# @bot.slash_command(name="loop", description="Toggles looping of the queue")
# async def loop_slash(ctx):
#     await loop(ctx)

@bot.slash_command(name="shuffle", description="Shuffeling of the queue")
async def shuffle_slash(ctx):
    await shuffle(ctx)

@bot.slash_command(name="ping", description="Checks the bot's latency")
async def ping_slash(ctx):
    await ping(ctx)

@bot.slash_command(name="pause", description="Pauses the currently playing audio")
async def pause_slash(ctx):
    await pause(ctx)

@bot.slash_command(name="resume", description="Resumes the currently paused audio")
async def resume_slash(ctx):
    await resume(ctx)

@bot.slash_command(
    name="force_play",
    description="Force plays the provided audio",
    options=[
        Option(
            name="query",
            description="The audio track to play",
            required=True,
            type=str,
        ),
        Option(
            name="insta_skip",
            description="Skip to the next track immediately",
            required=False,
            choices=[
                OptionChoice(name="Yes", value="true"),
                OptionChoice(name="No", value="false")
            ],
            type=str,
        ),
    ]
)
async def force_play_slash(ctx, query: str, insta_skip: str = "false"):
    insta_skip_bool = insta_skip == "true"
    await force_play(ctx, query=query, insta_skip=insta_skip_bool)

@bot.slash_command(name="help", description="Shows all available commands")
async def help_slash(ctx):
    await help(ctx)

@bot.slash_command(name="play", description="Plays the provided audio", options=[Option(name="query", required=True)])
async def play_slash(ctx, query: str):
    await play_command(ctx, query=query)

# if isServerRunning:
#     @bot.slash_command(
#         name="play_with_ai_voice",
#         description="A command to play with custom voice",
#         options=[
#             Option(  
#                 name="model",
#                 description="Choose a model",
#                 required=True,
#                 choices=[OptionChoice(name=choice, value=choice) for choice in model_choices],
#             ),
#             Option(
#                 name="index",
#                 description="Choose an index",
#                 required=True,
#                 choices=[OptionChoice(name=choice, value=choice) for choice in index_choices],
#             ),
#             Option(
#                 name="pitch",
#                 description="Enter a pitch",
#                 required=True,
#                 choices=[
#                     OptionChoice(name="↑12", value="12"),
#                     OptionChoice(name="↑6", value="6"),
#                     OptionChoice(name="0", value="0"),
#                     OptionChoice(name="↓6", value="-6"),
#                     OptionChoice(name="↓12", value="-12")
#                 ],
#                 type=int,
#             ),
#             Option(
#                 name="url",
#                 description="Enter a URL",
#                 required=True,
#                 type=str,
#             ),
#         ],
#     )
#     async def play_with_custom_voice(ctx, model: str, index: str, pitch: int, url: str):
#         async with websockets.connect('ws://localhost:8765', max_size=26_000_000) as websocket:
#             request_data = {
#                 "command": "generate_ai_cover",
#                 "model": model,
#                 "index": index,
#                 "pitch": pitch,
#                 "url": url
#             }
            
#             await websocket.send(json.dumps(request_data))
#             print(json.dumps(request_data))

#             message = await websocket.recv()
#             data = json.loads(message)

#             dc_message = await ctx.respond(embed=await embed_generator.create_embed("🗣️ AI Singer 🗣️", data["message"]))

#             # Listen for updates from the server
#             while True:
#                 message = await websocket.recv()
#                 data = json.loads(message)
#                 #print(data)
#                 if "message" in data:
#                     # Send a new message with the update
#                     await dc_message.edit(embed=await embed_generator.create_embed("AI Singer", data["message"]))
#                 elif "file" in data:
#                     file_data = base64.b64decode(data["file"])
#                     file_like_object = io.BytesIO(file_data)
#                     edited_message = await dc_message.edit(embed=await embed_generator.create_embed("AI Singer", "Finished"), file=discord.File(file_like_object, filename="unknown.mp3"))
#                     file_url = edited_message.attachments[0].url

#                     await play_command(ctx, query=file_url)
#                 elif "error" in data:
#                     await dc_message.edit(f"Error from server: {data['error']}")
#                 elif "queue_position" in data:
#                     await dc_message.edit(embed=await embed_generator.create_embed("AI Singer", f"Your request is at position {data['queue_position']} in the queue."))
#                 elif "status" in data:
#                     print("made it out")
#                     break

#         print("finished")

bot.run(os.getenv('DISCORD_TOKEN'))
