# Standard library imports
import asyncio
import base64
import io
import json
import os
import random
from enum import Enum
from typing import List

# Third-party imports
import discord
import websockets
from discord.commands import Option, OptionChoice
from discord.ext import commands
from dotenv import load_dotenv

# Local application imports
from discord_utils import embed_generator
from platform_handlers import audio_content_type_finder, music_platform_finder
from server_requests import rvc_server_pinger
from enums.status import Status
from models.guild_music_information import GuildMusicInformation

load_dotenv()

guilds_info = List[GuildMusicInformation]
model_choices = []

isServerRunning = rvc_server_pinger.check_connection()

if(isServerRunning):
    model_choices, index_choices = rvc_server_pinger.fetch_choices()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=[".", "!", "$"], intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name="to da kuhle songs"))
    user = await bot.fetch_user(566263212077481984)
    
    dm_channel = await user.create_dm()
    
    messages = await dm_channel.history().flatten()
    
    for msg in messages:
        await msg.delete()

    print(f"Bot is ready and logged in as {bot.user.name}")
    await user.send(f"Bot is ready and logged in as {bot.user.name}")

async def get_guild_music_information(guild_id: int) -> GuildMusicInformation:
    global guilds_info

    for guild in guilds_info:
        if guild.id is guild_id:
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

    new_guild = GuildMusicInformation(id=guild_id, voice_channel=voice_channel, voice_client=voice_client)
    guilds_info.append(new_guild)
    return new_guild

async def add_to_queue(guild_id, url):
    global guilds_info

    for guild in guilds_info:
        if guild.id == guild_id:
            guild.queue_object_list.append(url)

@bot.command(aliases=['next', 'advance', 'skip_song', 'move_on', 'play_next'])
async def skip(ctx):
    guild = get_guild_music_information(ctx.guild.id)

    if guild:
        guild.voice_client.stop()
    
    if ctx.message:
        await ctx.message.add_reaction("⏭️")
    else:
        await ctx.respond("Skipped Song ⏭️")

@bot.command(aliases=['exit', 'quit', 'bye', 'farewell', 'goodbye', 'leave_now', 'disconnect', 'stop_playing'])
async def leave(ctx):
    guild = get_guild_music_information(ctx.guild.id)

    if guild:
        guild.voice_client.stop()
        await delete_guild(guild.id)
    
    if ctx.message:
        await ctx.message.add_reaction("👋")
    else:
        await ctx.respond("Left the channel 👋")

@bot.command(aliases=['hold', 'freeze', 'break', 'wait', 'intermission'])
async def pause(ctx):
    guild = get_guild_music_information(ctx.guild.id)
        
    if guild:
        guild.voice_client.pause()
    
    if ctx.message:
        await ctx.message.add_reaction("⏸️")
    else:
        await ctx.respond("Paued the music ⏸️")

@bot.command(aliases=['continue', 'unpause', 'proceed', 'restart', 'go', 'resume_playback'])
async def resume(ctx):
    guild = get_guild_music_information(ctx.guild.id)

    if guild:
        guild.voice_client.resume()
    
    if ctx.message:
        await ctx.message.add_reaction("▶️")
    else:
        await ctx.respond("Resumed the music ▶️")

@bot.command(aliases=['lp', 'repeat', 'cycle', 'toggle_loop', 'toggle_repeat'])
async def loop(ctx):
    guild = get_guild_music_information(ctx.guild.id)

    if guild.loop_queue:
        if ctx.message:
            await ctx.message.add_reaction("🔄")
        else:
            await ctx.respond("Now looping the queue 🔄")
    else:
        if ctx.message:
            await ctx.message.add_reaction("⏹️")
        else:
            await ctx.respond("Stopped looping the queue ⏹️")

@bot.command(aliases=['fp', 'forceplay', 'playforce'])
async def force_play(ctx, *, query=None):
    guild = get_guild_music_information(ctx.guild.id)

    if guild.queue_object_list and guild.voice_client:
        guild.queue_object_list.insert(0, query)
        guild.voice_client.stop()  
    else:
        await ctx.send("No song is currently playing")
    
    if ctx.message:
        await ctx.message.add_reaction("⏭️")
    else:
        await ctx.respond("Force playing Song ⏭️")

@bot.command()
async def shuffle(ctx):
    guild = get_guild_music_information(ctx.guild.id)
    random.shuffle(guild.queue_object_list)

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
        ("stop", "Stops the currently playing audio"),
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

async def play(ctx, guild_id: int):
    global guilds_info
    guild = get_guild_music_information(guild_id)

    while guild.queue_object_list:
        guild.bot_status = Status.IS_PLAYING

        query = guild.queue_object_list.pop(0)

        try:
            songList = audio_content_type_finder.get_audio_content_type(query)

            if (len(songList) != 1):
                await ctx.send(embed=embed_generator.create_embed("📋 Adding Items to Queue 📋", f"Added **{len(songList)}** Songs"))
                for song in songList:
                    guild.queue_object_list.append(song)
                continue
        except Exception as e:
            await ctx.send("`An error occurred: {}`".format(e))
            continue

        try:
            toPlay = await music_platform_finder.find_platform(ctx, query)
        except Exception as e:
            await ctx.send("`An error occurred: {}`".format(e))
            continue

        if not toPlay:
            continue
        
        # Create an audio source and player
        audio_source = discord.FFmpegPCMAudio(toPlay.data.link, options='-vn', before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        player = discord.PCMVolumeTransformer(audio_source)

        # Play the audio
        guild.voice_client.play(player)
        try:
            await toPlay.message.edit(embed=embed_generator.create_embed("💿 Now Playing 💿", f"**{toPlay.data.song_name}** By **{toPlay.data.author}**", toPlay.data.image ))
        except:
            print("Error editing message")
            
        while guild.voice_client.is_playing() or guild.voice_client.is_paused():
            await asyncio.sleep(1)

        if not next((guild for guild in guilds_info if guild.id == guild_id), None):   
            break     
        
        if(guild.loop_queue):
            guild.queue_object_list.append(query)

    await guild.voice_client.disconnect()
    guild.bot_status = Status.IDLE
    guild.voice_client = None
    await delete_guild(ctx.guild.id)

@bot.command(name='play', aliases=['p', 'pl', 'play_song', 'queue', 'add', 'enqueue'])
async def play_command(ctx, *, query=None):

    # first_word = query.split()[0].lower() if query else None
    # if first_word == "earrape":
    #     await ctx.reply("The audio will play in earrape mode.")
    #     query = ' '.join(query.split()[1:])

    guild = await get_guild_music_information(ctx.guild.id) or await create_new_guild_music_information_and_join(ctx.guild.id, ctx.author.voice.channel)

    if guild.is_bot_busy:
        await add_to_queue(guild.id, query)
    else:
        await add_to_queue(guild.id, query)
        await play(ctx, guild.id)
        
        if ctx.message:
            await ctx.message.add_reaction("📥")
        else:
            await ctx.respond("Added to the queue 📥")

###################################################
################# SLASH COMMANDS ##################
###################################################

@bot.slash_command(name="skip", description="Skips the currently playing audio")
async def skip_slash(ctx):
    await skip(ctx)

@bot.slash_command(name="leave", description="Leaves the voice channel and stops playing audio")
async def leave_slash(ctx):
    await leave(ctx)

@bot.slash_command(name="loop", description="Toggles looping of the queue")
async def loop_slash(ctx):
    await loop(ctx)

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
    
@bot.slash_command(name="force_play", description="Force plays the provided audio", options=[Option(name="query", required=True)])
async def force_play_slash(ctx, query: str):
    await force_play(ctx, query=query)

@bot.slash_command(name="help", description="Shows all available commands")
async def help_slash(ctx):
    await help(ctx)

@bot.slash_command(name="play", description="Plays the provided audio", options=[Option(name="query", required=True)])
async def play_slash(ctx, query: str):
    await play_command(ctx, query=query)

if isServerRunning:
    @bot.slash_command(
        name="play_with_ai_voice",
        description="A command to play with custom voice",
        options=[
            Option(  
                name="model",
                description="Choose a model",
                required=True,
                choices=[OptionChoice(name=choice, value=choice) for choice in model_choices],
            ),
            Option(
                name="index",
                description="Choose an index",
                required=True,
                choices=[OptionChoice(name=choice, value=choice) for choice in index_choices],
            ),
            Option(
                name="pitch",
                description="Enter a pitch",
                required=True,
                choices=[
                    OptionChoice(name="↑12", value="12"),
                    OptionChoice(name="↑6", value="6"),
                    OptionChoice(name="0", value="0"),
                    OptionChoice(name="↓6", value="-6"),
                    OptionChoice(name="↓12", value="-12")
                ],
                type=int,
            ),
            Option(
                name="url",
                description="Enter a URL",
                required=True,
                type=str,
            ),
        ],
    )
    async def play_with_custom_voice(ctx, model: str, index: str, pitch: int, url: str):
        async with websockets.connect('ws://localhost:8765', max_size=26_000_000) as websocket:
            request_data = {
                "command": "generate_ai_cover",
                "model": model,
                "index": index,
                "pitch": pitch,
                "url": url
            }
            
            await websocket.send(json.dumps(request_data))
            print(json.dumps(request_data))

            message = await websocket.recv()
            data = json.loads(message)

            dc_message = await ctx.respond(embed=embed_generator.create_embed("🗣️ AI Singer 🗣️", data["message"]))

            # Listen for updates from the server
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                #print(data)
                if "message" in data:
                    # Send a new message with the update
                    await dc_message.edit(embed=embed_generator.create_embed("🗣️ AI Singer 🗣️", data["message"]))
                elif "file" in data:
                    file_data = base64.b64decode(data["file"])
                    file_like_object = io.BytesIO(file_data)
                    edited_message = await dc_message.edit(embed=embed_generator.create_embed("🗣️ AI Singer 🗣️", "Finished"), file=discord.File(file_like_object, filename="unknown.mp3"))
                    file_url = edited_message.attachments[0].url

                    await play_command(ctx, query=file_url)
                elif "error" in data:
                    await dc_message.edit(f"Error from server: {data['error']}")
                elif "queue_position" in data:
                    await dc_message.edit(embed=embed_generator.create_embed("🗣️ AI Singer 🗣️", f"Your request is at position {data['queue_position']} in the queue."))
                elif "status" in data:
                    print("made it out")
                    break

        print("finished")


bot.run(os.getenv('DISCORD_TOKEN'))
