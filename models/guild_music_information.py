from dataclasses import dataclass
from typing import List
import discord

from models.queue_object import QueueObject

@dataclass
class GuildMusicInformation:
  id: int
  voice_channel: discord.VoiceChannel
  voice_client: discord.VoiceClient
  is_bot_busy: bool
  queue: List[QueueObject]
  loop_queue: bool