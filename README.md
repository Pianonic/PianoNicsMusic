# <p align="center">PianoNic's Music Bot</p>
<p align="center">
  <img src="https://github.com/Pianonic/PianoNicsMusic/blob/main/image/Logo.png?raw=true" width="200" alt="PianoNic's Music Bot Logo">
</p>
<p align="center">
  <strong>Bring music to your Discord server with a smart, versatile bot.</strong>
  Built with Python and Pycord.
</p>
<p align="center">
  <a href="https://github.com/Pianonic/PianoNicsMusic"><img src="https://badgetrack.pianonic.ch/badge?tag=piano-nics-music&label=visits&color=2c234a&style=flat" alt="visits" /></a>
  <a href="https://github.com/Pianonic/PianoNicsMusic/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/License-CC%20BY--NC%204.0-2c234a.svg?style=flat" alt="License: CC BY-NC 4.0"/></a>
  <a href="https://github.com/Pianonic/PianoNicsMusic/releases"><img src="https://img.shields.io/github/v/release/Pianonic/PianoNicsMusic?include_prereleases&color=2c234a&label=Latest%20Release"/></a>
</p>

## 🚀 Features

- **🎵 Music Playback**: Play songs directly in your Discord server's voice channels
- **🌐 Flexible Sources**: Supports music from streaming services, URLs, and local files
- **🗣️ AI Voice Integration**: Unique feature to play music using a trained AI voice (In Development)
- **📜 Queue Management**: Add, remove, skip, loop, and shuffle tracks easily
- **👌 Simple Commands**: User-friendly slash commands for all music controls
- **🛡️ Stable & Reliable**: Built with robust error handling to keep the music playing
- **🐳 Docker Ready**: Easy deployment with pre-built Docker images

## 🛠️ Installation

### Using Docker (Recommended)

#### Option 1: Pull and Run a Pre-built Image
You can pull the latest pre-built image from Docker Hub or GitHub Container Registry.

**Docker Hub:**
```bash
docker pull pianonic/pianonicsmusic:latest
```

**GitHub Container Registry:**
```bash
docker pull ghcr.io/pianonic/pianonicsmusic:latest
```

Then, run the container with your bot token:
```bash
docker run -d --name pianonic-music-bot -e DISCORD_TOKEN=YOUR_DISCORD_TOKEN pianonic/pianonicsmusic:latest
```

#### Option 2: Run with Docker Compose (Recommended)
**1. Create a `.env` file:**  
Create a `.env` file in your project directory and add your credentials:
```properties
# Paste your bot token here
DISCORD_TOKEN=YOUR_DISCORD_TOKEN

# Optional: Add Spotify credentials for faster Spotify link loading
# Get them from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID=YOUR_SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET=YOUR_SPOTIFY_CLIENT_SECRET
```

**2. Create a `compose.yml` file:**  
Use your favorite editor to create a `compose.yml` file and paste this into it:
```yaml
services:
  pianonic-music-bot:
    image: pianonic/pianonicsmusic:latest # Uses the image from Docker Hub
    # image: ghcr.io/pianonic/pianonicsmusic:latest # Uses the image from GitHub Container Registry
    container_name: pianonic-music-bot
    env_file: .env
    restart: unless-stopped
```

**3. Start it:**
```bash
docker compose up -d
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/Pianonic/PianoNicsMusic.git
cd PianoNicsMusic

# Create a virtual environment
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure your bot token in config.ini or environment variables
# Run the bot
python main.py
```

## 🎧 Getting Started

### Step 1: Create Your Discord Bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and **log in**
2. Click **"New Application"** and give your bot a name (e.g., "My Music Bot")
3. On the left menu, go to the **"Bot"** tab
4. Click **"Reset Token"**, then **"Yes, do it!"**, and **copy the token**. This is your `DISCORD_TOKEN`. Keep it secret!
5. Go to the **"OAuth2" -> "URL Generator"** tab
6. Select the **`bot`** and **`applications.commands`** scopes
7. Under "Bot Permissions", choose **"Connect"** and **"Speak"**
8. **Copy the generated URL** at the bottom, paste it into your browser, and invite the bot to your server

### Step 2: Deploy the Bot
Follow the installation instructions above to deploy your bot using Docker or manual installation.

> **Note:** The bot works without Spotify credentials, but they are highly recommended to make Spotify links load up to 60% faster.

## 🛠️ Usage

Control the bot with these simple slash commands in your server's text channels.

### 🎵 Music Playback

| Command | Aliases | Description | Example |
| :--- | :--- | :--- | :--- |
| `play` | `p`, `pl`, `play_song`, `add`, `enqueue` | Plays a song, adds to queue, or loads from a file. | `play Never Gonna Give You Up` |
| `pause` | `hold`, `freeze`, `break`, `wait`, `intermission` | Pauses the current song. | `pause` |
| `resume` | `continue`, `unpause`, `proceed`, `restart`, `go`, `resume_playback` | Resumes playback. | `resume` |
| `force_play` | `fp`, `forceplay`, `playforce` | Plays a song right after the current one finishes. | `force_play My Favorite Song` |

### �️ Queue Management

| Command | Aliases | Description | Example |
| :--- | :--- | :--- | :--- |
| `skip` | `next`, `advance`, `skip_song`, `move_on`, `play_next` | Skips to the next song. | `skip` |
| `stop` | | Stops music, clears queue, disconnects bot. | `stop` |
| `leave` | `exit`, `quit`, `bye`, `farewell`, `goodbye`, `leave_now`, `disconnect`, `stop_playing` | Leaves the voice channel and stops playing audio. | `leave` |
| `loop` | `lp`, `repeat`, `cycle`, `toggle_loop`, `toggle_repeat` | Toggles looping for the entire queue. | `loop` |
| `shuffle` | | Toggles randomizing the queue order. | `shuffle` |
| `bot_status` | `status`, `current`, `now_playing` | Shows current song and upcoming queue. | `bot_status` |
| `queue` | `q`, `show_queue`, `list`, `queue_list` | Shows the full music queue. | `queue` |

### 🤖 General Commands

| Command | Aliases | Description | Example |
| :--- | :--- | :--- | :--- |
| `help` | `h`, `commands`, `command`, `cmds`, `cmd`, `info`, `assist`, `assistme`, `helpme`, `helppls`, `helpmepls`, `helpmeplease`, `helpmeout`, `helpmeoutpls`, `helpmeoutplease` | Shows a list of all commands. | `help` |
| `ping` | | Checks the bot's response time. | `ping` |
| `information` | `v`, `ver`, `version` | Displays bot version and system info. | `information` |

## ⚙️ Technical Details

### Bot Features
- Built with Pycord for reliable Discord integration
- Supports multiple audio sources and formats
- Queue management with loop and shuffle functionality
- AI voice integration capabilities (in development)
- Robust error handling and automatic recovery

## 📦 Requirements
- Python 3.13+
- Docker (for Docker installation)
- Discord Bot Token
- Dependencies: Shown in [requirements.txt](./requirements.txt)

## 🔧 Troubleshooting
- **Bot won't connect?** Make sure you invited it with "Connect" and "Speak" permissions, and that you are in a voice channel when using the `/play` command
- **Bot is offline?** If using Docker, run `docker compose ps` to check. If not running, use `docker compose logs` for details
- **Songs fail to play?** The bot automatically skips problem songs. This can happen if a song is region-locked or unavailable

## 📄 License
This project is licensed under the CC BY-NC 4.0 License.
See the [LICENSE.md](https://github.com/Pianonic/PianoNicsMusic/blob/main/LICENSE.md) file for more details.

---
<p align="center">Made with ❤️ by <a href="https://github.com/Pianonic">Pianonic</a></p>
