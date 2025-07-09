<p align="center">
  <img src="https://github.com/Pianonic/PianoNicsMusic/blob/main/image/Logo.png?raw=true" alt="PianoNic's Music Bot" width="200"/>
</p>

# <p align="center">🎹 PianoNic's Music Bot</p>

<p align="center">
  <strong>Bring music to your Discord server with a smart, versatile bot.</strong>
</p>

<p align="center">
  <a href="https://github.com/Pianonic/PianoNicsMusic"><img src="https://badgetrack.pianonic.ch/badge?url=https://github.com/Pianonic/PianoNicsMusic&label=Visits&color=2c234a&style=flat&logo=github" alt="Visitor Count"/></a>
  <a href="https://github.com/Pianonic/PianoNicsMusic/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/License-CC%20BY--NC%204.0-2c234a.svg"/></a>
  <a href="https://hub.docker.com/r/pianonic/pianonicsmusic"><img src="https://img.shields.io/badge/Docker_Hub-pianonic/pianonicsmusic-2c234a.svg?logo=docker"/></a>
  <a href="https://github.com/Pianonic/PianoNicsMusic/pkgs/container/pianonicsmusic"><img src="https://img.shields.io/badge/GitHub-ghcr.io-2c234a.svg?logo=github"/></a>
</p>

---

## 🎶 About PianoNic's Music Bot

PianoNic's Music Bot lets you play your favorite songs directly in your Discord server's voice channels. It supports music from almost any source and features a unique (and developing) AI voice integration for a new listening experience.

## 🌟 Key Features

*   **🎵 Music Playback:** Play songs directly in your Discord server.
*   **🌐 Flexible Sources:** Supports music from streaming services, URLs, and local files.
*   **🗣️ AI Voice (In Development):** A unique feature to play music using a trained AI voice.
*   **📜 Easy Queue Management:** Add, remove, skip, loop, and shuffle tracks easily.
*   **👌 Simple Commands:** User-friendly commands for all music controls.
*   **🛡️ Stable & Reliable:** Built with robust error handling to keep the music playing.

## 🚀 Get Started in 3 Steps!

Follow these quick steps to get your bot online.

### Step 1: Create Your Discord Bot

1.  Go to the [Discord Developer Portal](https://discord.com/developers/applications) and **log in**.
2.  Click **"New Application"** and give your bot a name (e.g., "My Music Bot").
3.  On the left menu, go to the **"Bot"** tab.
4.  Click **"Reset Token"**, then **"Yes, do it!"**, and **copy the token**. This is your `DISCORD_TOKEN`. Keep it secret!
5.  Go to the **"OAuth2" -> "URL Generator"** tab.
6.  Select the **`bot`** and **`applications.commands`** scopes.
7.  Under "Bot Permissions", choose **"Connect"** and **"Speak"**.
8.  **Copy the generated URL** at the bottom, paste it into your browser, and invite the bot to your server.

### Step 2: Configure Your Bot Files

You need two files: `.env` for your bot's credentials and `compose.yml` to run it.

1.  Create a new folder on your computer (e.g., `my-music-bot`).
2.  Inside this new folder, create a file named `.env` and add the following content, replacing the placeholders:

    ```properties
    # Paste your bot token here
    DISCORD_TOKEN=YOUR_DISCORD_TOKEN

    # Optional: Add Spotify credentials for faster Spotify link loading.
    # Get them from https://developer.spotify.com/dashboard
    SPOTIFY_CLIENT_ID=YOUR_SPOTIFY_CLIENT_ID
    SPOTIFY_CLIENT_SECRET=YOUR_SPOTIFY_CLIENT_SECRET
    ```

3.  In the *same folder*, create a file named `compose.yml` and copy-paste this entire content into it:

    ```yaml
    services:
      pianonic-music-bot:
        # Pulls the latest image from Docker Hub (recommended)
        image: pianonic/pianonicsmusic:latest
        # To use the GitHub image instead, comment the line above and uncomment this one:
        # image: ghcr.io/pianonic/pianonicsmusic:latest
        container_name: pianonic-music-bot
        env_file: .env
        restart: unless-stopped
    ```

    > **Note:** The bot works without Spotify credentials, but they are highly recommended to make Spotify links load up to 60% faster.

## 📦 Run Your Bot (Easiest Way: Docker)

Docker is the recommended and simplest way to run your bot, as it uses pre-built versions.

1.  **Make sure you have Docker and Docker Compose installed.**
2.  **In your `my-music-bot` folder, open a terminal or command prompt and run:**

    ```sh
    docker-compose up -d
    ```

    Docker will automatically download and start your bot in the background. Your bot is now online!

<details>
<summary><strong>Advanced: Manual Python Setup (if you prefer not to use Docker)</strong></summary>

Use this method if you want to run the bot directly with Python.

1.  **Clone the full repository:**
    ```sh
    git clone https://github.com/Pianonic/PianoNicsMusic.git
    cd PianoNicsMusic
    ```
2.  **Make sure you have Python 3.8+ installed.**
3.  **Install the required libraries:**
    ```sh
    pip install -r requirements.txt
    ```
4.  **Run the bot:**
    ```sh
    python main.py
    ```

</details>

## 🎧 How to Use Commands

Control the bot with these simple commands in your server's text channels.

### 🎵 Music Playback

| Command | Aliases | Description | Example |
| :--- | :--- | :--- | :--- |
| `play` | `p`, `add` | Plays a song, adds to queue, or loads from a file. | `play Never Gonna Give You Up` |
| `pause` | `hold` | Pauses the current song. | `pause` |
| `resume` | `unpause` | Resumes playback. | `resume` |
| `force_play` | `fp` | Plays a song right after the current one finishes. | `force_play My Favorite Song` |

### 🇶 Queue Management

| Command | Aliases | Description | Example |
| :--- | :--- | :--- | :--- |
| `skip` | `next` | Skips to the next song. | `skip` |
| `stop` | `leave` | Stops music, clears queue, disconnects bot. | `stop` |
| `loop` | `repeat` | Toggles looping for the entire queue. | `loop` |
| `shuffle` | | Toggles randomizing the queue order. | `shuffle` |
| `bot_status` | `status`, `np` | Shows current song and upcoming queue. | `bot_status` |
| `queue` | `q`, `show_queue` | Shows the full music queue. | `queue` |

### 🤖 General Commands

| Command | Aliases | Description | Example |
| :--- | :--- | :--- | :--- |
| `help` | `h`, `commands` | Shows a list of all commands. | `help` |
| `ping` | | Checks the bot's response time. | `ping` |
| `information` | `v`, `version` | Displays bot version and system info. | `information` |

---

## 🔧 Troubleshooting Tips

*   **Bot won't connect?** Make sure you invited it with "Connect" and "Speak" permissions (Step 1.8), and that you are in a voice channel when using the `play` command.
*   **Bot is offline?** If using Docker, run `docker-compose ps` to check. If not running, use `docker-compose logs` for details.
*   **Songs fail to play?** The bot automatically skips problem songs. This can happen if a song is region-locked or unavailable.

## 📄 License

This project is licensed under the [CC BY-NC 4.0](LICENSE.md).

---

<p align="center">Made with ❤️ by <a href="https://github.com/Pianonic">Pianonic</a></p>
