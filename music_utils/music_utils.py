from typing import List

import ddl_retrievers.soundcloud_ddl_retriever
import ddl_retrievers.spotify_ddl_retriever
import ddl_retrievers.tiktok_ddl_retriever
import ddl_retrievers.universal_ddl_retriever
import ddl_retrievers.unknown_source_ddl_retriever
import ddl_retrievers
from extracting_utils import spotify_playlist_extractor
from models.music_information import MusicInformation
from enums.audio_content_type import AudioContentType
from enums.source import Source
import yt_dlp

import music_utils.audio_content_type_finder as ACTF
import music_utils.music_source_finder as MSF
from searching_utils import query_to_youtube

async def get_streaming_url(query_url: str) -> MusicInformation:
    source = await MSF.find_music_source(query_url)

    if source is Source.SPOTIFY:
        return await ddl_retrievers.spotify_ddl_retriever.get_streaming_url(query_url)

    elif source is Source.TIK_TOK:
        return await ddl_retrievers.tiktok_ddl_retriever.get_streaming_url(query_url)

    elif source is Source.SOUND_CLOUD:       
        return await ddl_retrievers.soundcloud_ddl_retriever.get_streaming_url(query_url)

    elif source is Source.UNKNOWN_SOURCE:
        return await ddl_retrievers.unknown_source_ddl_retriever.get_streaming_url(query_url)
        
    else:
        raise Exception(f"Unsupported source: {source}. The URL provided does not match any known music sources.")

async def retrieve_media_links(query: str) -> List[str]:
    source = await MSF.find_music_source(query)
    audio_content_type: AudioContentType = await ACTF.get_audio_content_type(query, source)

    if audio_content_type is AudioContentType.NOT_SUPPORTED:
        raise Exception(f"Audio content type '{audio_content_type}' for the query '{query}' is not supported for source '{source}'.")
    
    elif audio_content_type is AudioContentType.QUERY:
        return [await query_to_youtube.get_song_url(query)]
    
    elif audio_content_type is AudioContentType.SINGLE_SONG:
        return [query]
    
    # Tik Tok
    elif source is Source.TIK_TOK:
        return [query]

    # Spotify Playlist
    elif source is Source.SPOTIFY:
        return await spotify_playlist_extractor.get_song_urls(query)    

    # Other Playlists 
    else:
        ydl_opts = {
            'extract_flat': True,
            'quiet': True,
            'skip_download': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(query)
            entries = playlist_info.get("entries", None)

            if entries:
                return [entry['url'] for entry in entries]
            else:
                raise Exception(f"Failed to extract URLs using yt_dlp for query: {query}")