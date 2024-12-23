<p align="center">
  <img src="https://github.com/Pianonic/PianoNicsMusic/blob/main/image/Logo.png?raw=true" alt="PianoNic's Music Bot" width="200"/>
</p>

# 🎹 PianoNic's Music Bot

## Description 🎶
PianoNic's Music Bot is a versatile Discord bot designed to elevate the music experience on your Discord server. It allows you to play your favorite tracks on command and includes a unique feature that uses a trained AI voice to play music, providing a novel and engaging musical experience. Additionally, the bot can play music from virtually any source, offering unparalleled flexibility.

## Features 🌟
- **🎵 Music Playback:** Play music directly in your Discord server's voice channels.
- **🗣️ AI Voice Integration:** Use a trained AI voice to play music for a distinctive listening experience. (In developpment)
- **🌐 Universal Source Playback:** Play music from any source, including streaming services, URLs, and local files.
- **📜 Queue System:** Manage music playback with an intuitive queue system—add, remove, or skip tracks effortlessly.
- **👌 Easy Commands:** Simple, user-friendly commands for controlling music playback and utilizing AI voice features.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/Pianonic/PianoNicsMusic.git
    cd PianoNicsMusic
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the bot**:
    ```sh
    python main.py
    ```

## Configuration

1. **Create a `.env` file** in the root directory:
    ```properties
    DISCORD_TOKEN=YOUR_DISCORD_TOKEN
    SPOTIFY_CLIENT_ID=YOUR_SPOTIFY_CLIENT_ID
    SPOTIFY_CLIENT_SECRET=YOUR_SPOTIFY_CLIENT_SECRET
    ```

2. **Obtain Spotify Credentials** (Optional):
    - Visit the [Spotify Developer Dashboard](https://developer.spotify.com/documentation/web-api/concepts/apps) to create an application and obtain your `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`.

> **Note:** Providing Spotify credentials is **optional**. The bot will still function without them. However, when credentials are provided, the bot will load Spotify songs **60% faster**, as it can directly access Spotify's API for optimized track info retrieval.

## Docker Setup 🐳

1. **Build the Docker Image**:
    ```sh
    docker build -t pianonic-music-bot .
    ```

2. **Run the Docker Container**:
    ```sh
    docker run -d --name pianonic-music-bot pianonic-music-bot
    ```

3. **Using Docker Compose** (optional):
    Create a `docker-compose.yml` for simplified container management:
    ```yaml
    version: '3.8'

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

    Run with:
    ```sh
    docker-compose up --build -d
    ```

## Usage 🚀
- **▶️ Playing Music:** Use the `play` command followed by the song name, URL, or file path to queue music.
- **🎤 AI Voice Music:** Activate the AI voice feature for a unique music playback experience. (In developpment)
- **🔀 Managing the Queue:** Use commands to add, remove, or skip tracks in the queue.

## Contributing 🤝
We welcome contributions to PianoNic's Music Bot! Please fork the repository, make your changes, and submit a pull request.

## License 📄
This project is licensed under the [CC BY-NC 4.0](LICENSE.md).
