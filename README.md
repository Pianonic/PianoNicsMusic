<p align="center">
  <img src="https://github.com/Pianonic/PianoNicsMusic/blob/main/image/Logo.png?raw=true" alt="PianoNic's Music Bot" width="200"/>
</p>

# <p align="center">🎹 PianoNic's Music Bot</p>

<p align="center">
  <strong>Elevate your Discord server's music experience with a versatile, AI-powered bot.</strong>
</p>

<p align="center">
  <a href="https://github.com/Pianonic/PianoNicsMusic"><img src="https://badgetrack.pianonic.ch/badge?url=https://github.com/Pianonic/PianoNicsMusic&label=Visits&color=2c234a&style=flat&logo=github" alt="Visitor Count"/></a>
  <a href="https://github.com/Pianonic/PianoNicsMusic/blob/main/LICENSE.md"><img src="https://img.shields.io/badge/License-CC%20BY--NC%204.0-2c234a.svg"/></a>
  <a href="https://hub.docker.com/r/pianonic/pianonicsmusic"><img src="https://img.shields.io/badge/Docker_Hub-pianonic/pianonicsmusic-2c234a.svg?logo=docker"/></a>
  <a href="https://github.com/Pianonic/PianoNicsMusic/pkgs/container/pianonicsmusic"><img src="https://img.shields.io/badge/GitHub-ghcr.io-2c234a.svg?logo=github"/></a>
  <a><img src="https://img.shields.io/badge/Python-3.8+-2c234a.svg"/></a>
</p>

---

## 🎶 What is PianoNic's Music Bot?

PianoNic's Music Bot is a versatile Discord bot designed to elevate the music experience on your server. It allows you to play your favorite tracks on command from virtually any source, offering unparalleled flexibility. It also includes a unique (and currently in-development) feature that uses a trained AI voice to play music, providing a novel and engaging musical experience.

## 🌟 Features

-   **🎵 Music Playback:** Play music directly in your Discord server's voice channels.
-   **🗣️ AI Voice Integration:** Use a trained AI voice to play music for a distinctive listening experience. (In development)
-   **🌐 Universal Source Playback:** Play music from any source, including streaming services, URLs, and local files.
-   **📜 Queue System:** Manage music playback with an intuitive queue system—add, remove, or skip tracks effortlessly.
-   **👌 Easy Commands:** Simple, user-friendly commands for controlling music playback and utilizing AI voice features.
-   **🛡️ Enhanced Error Handling:** Robust error recovery prevents the bot from getting stuck during playback issues.
-   **📊 Status Monitoring:** Real-time bot status and queue information commands.
-   **🔄 Version Management:** Built-in versioning system with detailed release information.

## 🚀 Getting Started (Setup in 3 Steps)

Follow these steps to get your bot up and running.

### Step 1: Create Your Discord Bot

Before you can run the code, you need to create a "Bot Application" in Discord.

1.  Go to the [Discord Developer Portal](https://discord.com/developers/applications) and log in.
2.  Click **"New Application"** and give it a name (e.g., "My Music Bot").
3.  Go to the **"Bot"** tab on the left menu.
4.  Click **"Reset Token"** and then **"Yes, do it!"**.
5.  **Copy the token!** This is your `DISCORD_TOKEN`. Keep it safe.
6.  Go to the **"OAuth2" -> "URL Generator"** tab.
7.  Select the `bot` and `applications.commands` scopes.
8.  In the "Bot Permissions" box that appears, select **"Connect"** and **"Speak"**.
9.  Copy the generated URL at the bottom, paste it into your browser, and invite the bot to your server.

### Step 2: Get the Necessary Files

You don't need to clone the whole repository to run the bot. You only need two files.

1.  Create a new folder on your computer (e.g., `my-music-bot`).
2.  Download the [`compose.yml`](https://raw.githubusercontent.com/Pianonic/PianoNicsMusic/main/compose.yml) file into that folder.
    *   *Right-click the link and "Save Link As..."*

### Step 3: Configure Your Bot

In the same folder, create a file named `.env` and add your credentials.

```properties
# Paste the bot token you copied from the Discord Developer Portal
DISCORD_TOKEN=YOUR_DISCORD_TOKEN

# These are optional, but make Spotify links load 60% faster!
# Get them from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID=YOUR_SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET=YOUR_SPOTIFY_CLIENT_SECRET
```

> **Note:** The bot works without Spotify credentials, but they are recommended for the best performance with Spotify links.

## 📦 Installation & Running the Bot

Choose one of the two methods below. Docker is the easiest and highly recommended.

### Option 1: Docker Setup (Easiest Method)

This method uses pre-built images from Docker Hub or GitHub, so you don't have to build anything. It's the fastest way to get started.

1.  **Make sure you have Docker and Docker Compose installed.**
2.  Open the `compose.yml` file you downloaded. It's already configured to pull the latest image. By default, it uses the image from Docker Hub:

    ```yaml
    services:
      pianonic-music-bot:
        # Pulls the latest image from Docker Hub
        image: pianonic/pianonicsmusic:latest
        # To use the GitHub image instead, comment the line above and uncomment this one:
        # image: ghcr.io/pianonic/pianonicsmusic:latest
        container_name: pianonic-music-bot
        env_file: .env
        restart: unless-stopped
    ```

3.  **Run the bot with one command:**

    ```sh
    docker-compose up -d
    ```

Docker will automatically download the latest version of the bot and run it in the background. Your bot is now online!

<details>
<summary><strong>Advanced: Building the Docker Image from Source</strong></summary>

If you have cloned the full repository and made changes to the source code, you'll need to build the image yourself.

1.  Clone the repository: `git clone https://github.com/Pianonic/PianoNicsMusic.git`
2.  Navigate into the directory: `cd PianoNicsMusic`
3.  Modify the `docker-compose.yml` to use the `build` command instead of `image`:
    ```yaml
    services:
      pianonic-music-bot:
        build:
          context: .
        container_name: pianonic-music-bot
        env_file: .env
        restart: unless-stopped
    ```
4.  Build and run your custom version:
    ```sh
    docker-compose up --build -d
    ```

</details>

### Option 2: Standard Python Setup (Manual)

Use this method if you prefer not to use Docker.

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

## 🎧 Usage: How to Use Commands

Control the bot with simple commands in your server's text channels.

### 🎵 Music Playback

| Command | Aliases | Description | Example |
| :--- | :--- | :--- | :--- |
| `play` | `p`, `add` | Plays a song, adds it to the queue, or loads a list of URLs from an attached file. | `play Never Gonna Give You Up`<br>`play` + file attachment |
| `pause` | `hold` | Pauses the currently playing song. | `pause` |
| `resume` | `unpause` | Resumes playback if paused. | `resume` |
| `force_play` | `fp` | Plays a song immediately after the current one finishes. | `force_play My Favorite Song`<br>`force_play` + file attachment |

### 🇶 Queue Management

| Command | Aliases | Description | Example |
| :--- | :--- | :--- | :--- |
| `skip` | `next` | Skips the current song and plays the next in queue. | `skip` |
| `stop` | `leave` | Stops the music, clears the queue, and disconnects the bot. | `stop` |
| `loop` | `repeat` | Toggles looping for the entire queue. | `loop` |
| `shuffle` | | Toggles shuffle mode, randomizing the queue order. | `shuffle` |
| `bot_status` | `status`, `np` | Shows the current song and the upcoming queue. | `bot_status` |
| `queue` | `q`, `show_queue`, `list`, `queue_list` | Shows the current music queue. | `queue` |

### 🤖 General Commands

| Command | Aliases | Description | Example |
| :--- | :--- | :--- | :--- |
| `help` | `h`, `commands` | Shows a list of all available commands. | `help` |
| `ping` | | Checks the bot's response time to Discord. | `ping` |
| `information` | `v`, `version` | Displays the bot's version and system info. | `information` |

---

## 🔧 Troubleshooting

-   **Bot won't connect to voice channel?** Make sure you invited it with the correct permissions (Step 1.8) and that you are in a voice channel when you use the `play` command.
-   **Bot is offline?** If using Docker, run `docker-compose ps` to check the container status. If it's not running, check the logs with `docker-compose logs`.
-   **Songs fail to play?** The bot will automatically skip failed songs. This can happen if a song is region-locked or the source is unavailable.

## 📄 License

This project is licensed under the [CC BY-NC 4.0](LICENSE.md).

---

<p align="center">Made with ❤️ by <a href="https://github.com/Pianonic">Pianonic</a></p>
