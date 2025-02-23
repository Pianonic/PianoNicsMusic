from urllib.parse import ParseResult, urlparse
import aiohttp
from bs4 import BeautifulSoup
from ddl_retrievers import universal_ddl_retriever
from models.music_information import MusicInformation


async def get_streaming_url(soundcloud_url) -> MusicInformation:
    parsed_url: ParseResult = urlparse(soundcloud_url)
    subdomain = parsed_url.hostname.split('.')[0]

    sc_url = soundcloud_url

    if "api" in subdomain:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://w.soundcloud.com/player/?url={soundcloud_url}") as response:
                html_content = await response.text()

                soup = BeautifulSoup(html_content, 'html.parser')

                canonical_link = soup.find('link', rel='canonical')
                if canonical_link:
                    href = canonical_link.get('href')
                    sc_url = href

    return await universal_ddl_retriever.get_streaming_url(sc_url)
