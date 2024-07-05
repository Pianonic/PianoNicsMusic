from dataclasses import dataclass
from typing import List
import discord

@dataclass
class GuildMusicInformation:
  id: int
  voice_channel: discord.VoiceChannel
  voice_client: discord.VoiceClient
  is_bot_busy: bool
  queue_object_list: List[str]
  loop_queue: bool