import os
from urllib.parse import urlparse
import requests
from ddl_retrievers import universal_ddl_retriever
from models.music_information import MusicInformation

async def get_streaming_url(unknown_url) -> MusicInformation:    
    response = requests.get(unknown_url)
    contentType = response.headers['content-type']

    if "audio" in contentType or "video" in contentType:
        parsed_url = urlparse(unknown_url)
        song_name = os.path.basename(parsed_url.path)
        
        return MusicInformation(unknown_url, song_name, "unkown", 'https://image.similarpng.com/very-thumbnail/2020/12/Popular-Music-icon-in-round-black-color-on-transparent-background-PNG.png')
    else:
        return await universal_ddl_retriever.get_streaming_url(unknown_url)
