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
  <a href="https://github.com/Pianonic/PianoNicsMusic?tab=readme-ov-file#-installation--setup"><img src="https://img.shields.io/badge/Selfhost-Instructions-2c234a.svg"/></a>
  <a href="https://github.com/Pianonic/PianoNicsMusic/releases/latest"><img src="https://img.shields.io/github/v/release/Pianonic/PianoNicsMusic?label=Version&color=2c234a.svg" alt="Latest Release"/></a>
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

## 📦 Installation & Setup

### 1. Clone the Repository

```sh
git clone https://github.com/Pianonic/PianoNicsMusic.git
cd PianoNicsMusic
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure the Bot

Create a `.env` file in the root directory with the following content:

```properties
DISCORD_TOKEN=YOUR_DISCORD_TOKEN
SPOTIFY_CLIENT_ID=YOUR_SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET=YOUR_SPOTIFY_CLIENT_SECRET
```

To get your Spotify credentials, visit the [Spotify Developer Dashboard](https://developer.spotify.com/documentation/web-api/concepts/apps) to create an application.

> **Note:** Providing Spotify credentials is **optional**. The bot will still function without them. However, when credentials are provided, the bot will load Spotify songs **60% faster**, as it can directly access Spotify's API for optimized track info retrieval.

### 4. Run the Bot

```sh
python main.py
```

## 🐳 Docker Setup

### Building and Running Locally (Docker)

These steps will build the Docker image from your local `Dockerfile` and run it.

1.  **Build the Docker Image:**

    ```sh
    docker build -t pianonic-music-bot .
    ```

2.  **Run the Docker Container:**

    ```sh
    docker run -d --name pianonic-music-bot pianonic-music-bot
    ```

### Using Docker Compose (Local Build)

This method simplifies managing the bot's Docker container, building the image from your local source.

Create a `docker-compose.yml` for simplified container management:

```yaml
services:
  pianonic-music-bot:
    build:
      context: .
    container_name: pianonic-music-bot
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - SPOTIFY_CLIENT_ID=${SPOTIFY_CLIENT_ID}
      - SPOTIFY_CLIENT_SECRET=${SPOTIFY_CLIENT_SECRET}
    restart: unless-stopped
```

Then, run it with:

```sh
docker-compose up --build -d
```

### Using Pre-built Images from a Registry (Recommended for Deployment)

For easier deployment and distribution, you can publish your Docker image to a container registry (like Docker Hub or GitHub Container Registry) and then pull it directly.

#### Step 1: Publish Your Docker Image (One-Time Setup)

Choose one of the following methods to publish your image. *Replace placeholders like `YOUR_GITHUB_USERNAME` with your actual GitHub username.*

**A. Publishing to Docker Hub:**

1.  **Log in to Docker Hub:**
    ```sh
    docker login
    ```
    (Enter your Docker Hub username and password when prompted.)

2.  **Tag your locally built image:**
    ```sh
    docker tag pianonic-music-bot:latest pianonic/pianonicsmusic:latest
    ```

3.  **Push the image to Docker Hub:**
    ```sh
    docker push pianonic/pianonicsmusic:latest
    ```

**B. Publishing to GitHub Container Registry (GHCR):**

1.  **Generate a Personal Access Token (PAT):**
    *   Go to GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic).
    *   Click "Generate new token".
    *   Ensure the `write:packages` scope is selected (this is crucial for pushing images).
    *   Copy the generated token immediately, as you won't see it again.

2.  **Log in to GHCR:**
    ```sh
    echo YOUR_GITHUB_PAT | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
    ```

3.  **Tag your locally built image:**
    Tag it with the GHCR format:
    ```sh
    docker tag pianonic-music-bot:latest ghcr.io/pianonic/pianonicsmusic:latest
    ```

4.  **Push the image to GHCR:**
    ```sh
    docker push ghcr.io/pianonic/pianonicsmusic:latest
    ```

#### Step 2: Update `docker-compose.yml` to Pull from Registry

Once your image is published, modify your `docker-compose.yml` to use the `image` directive instead of `build`.

**Option 1: Using Docker Hub Image**

```yaml
services:
  pianonic-music-bot:
    image: pianonic/pianonicsmusic:latest # Image pulled from Docker Hub
    container_name: pianonic-music-bot
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - SPOTIFY_CLIENT_ID=${SPOTIFY_CLIENT_ID}
      - SPOTIFY_CLIENT_SECRET=${SPOTIFY_CLIENT_SECRET}
    restart: unless-stopped
```

**Option 2: Using GitHub Container Registry (GHCR) Image**

```yaml
services:
  pianonic-music-bot:
    image: ghcr.io/pianonic/pianonicsmusic:latest # Image pulled from GitHub Container Registry
    container_name: pianonic-music-bot
    environment:
      - DISCORD_TOKEN=${DISCORD_TOKEN}
      - SPOTIFY_CLIENT_ID=${SPOTIFY_CLIENT_ID}
      - SPOTIFY_CLIENT_SECRET=${SPOTIFY_CLIENT_SECRET}
    restart: unless-stopped
```

**Run with the updated Compose file:**

```sh
docker-compose up -d
```
Docker Compose will now pull the specified image from the registry and run it.

## 🚀 Usage

### 🎵 Basic Commands

-   **▶️ Playing Music:** Use the `play` command followed by the song name, URL, or file path to queue music.
-   **🎤 AI Voice Music:** Activate the AI voice feature for a unique music playback experience. (In development)
-   **🔀 Managing the Queue:** Use commands to add, remove, or skip tracks in the queue.

### 📋 Available Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `play <query>` | `p`, `pl`, `play_song`, `queue`, `add`, `enqueue` | Play music from URL, search query, or playlist |
| `skip` | `next`, `advance`, `skip_song`, `move_on`, `play_next` | Skip the currently playing song |
| `pause` | `hold`, `freeze`, `break`, `wait`, `intermission` | Pause the current song |
| `resume` | `continue`, `unpause`, `proceed`, `restart`, `go`, `resume_playback` | Resume paused playback |
| `leave` | `exit`, `quit`, `bye`, `farewell`, `goodbye`, `leave_now`, `disconnect`, `stop_playing` | Leave voice channel and clear queue |
| `stop` | | Stop playing and leave voice channel (same as leave) |
| `loop` | `lp`, `repeat`, `cycle`, `toggle_loop`, `toggle_repeat` | Toggle queue looping |
| `shuffle` | | Toggle queue shuffling |
| `force_play <query>` | `fp`, `forceplay`, `playforce` | Add song to front of queue (with optional instant skip) |
| `bot_status` | `status`, `current`, `now_playing` | Show current bot and queue status |
| `information` | `v`, `ver`, `version` | Display bot version and system information |
| `help` | `h`, `commands`, `command`, `cmds`, `cmd`, `info`, `assist`, `assistme`, `helpme`, `helppls`, `helpmepls`, `helpmeplease`, `helpmeout`, `helpmeoutpls`, `helpmeoutplease` | Show all available commands |
| `ping` | | Check bot latency |

### 🎛️ Queue Management

- **Add Songs:** Use `play <song name or URL>` to add songs to the queue
- **Skip Songs:** Use `skip` to move to the next song
- **Loop Queue:** Use `loop` to repeat the entire queue
- **Shuffle Mode:** Use `shuffle` to randomize playback order
- **Force Play:** Use `force_play <song>` to play a song immediately after the current one

## 🔧 Troubleshooting

### Common Issues

**Bot gets stuck and won't play the next song:**
- This has been fixed in v1.2.0 with enhanced error handling
- Use the `skip` command to force move to the next song
- Use `bot_status` to check the current queue state

**Bot won't connect to voice channel:**
- Ensure the bot has proper permissions in your Discord server
- Make sure you're in a voice channel when using the `play` command
- Check that the bot has "Connect" and "Speak" permissions

**Songs fail to play:**
- The bot will automatically skip failed songs and continue with the queue
- Check your internet connection
- Some URLs might be region-restricted or unavailable

**Database issues:**
- The bot now uses a persistent database (`bot_data.db`)
- If issues persist, you can safely delete this file to reset the bot's state

### Getting Help

- Use the `help` command to see all available commands
- Use `bot_status` to check the current bot state
- Use `version` to check your bot version and ensure you have the latest updates

## 📄 License

This project is licensed under the [CC BY-NC 4.0](LICENSE.md).

---

<p align="center">Made with ❤️ by <a href="https://github.com/Pianonic">Pianonic</a></p>
