import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from platform_handlers import music_url_getter
from enums.platform import Platform
from enums.audio_content_type import AudioContentType

class TestMusicUrlGetter(unittest.IsolatedAsyncioTestCase):
    @patch('platform_handlers.music_url_getter.find_platform', new_callable=AsyncMock)
    @patch('platform_handlers.music_url_getter.ddl_retrievers.spotify_ddl_retriever.get_streaming_url', new_callable=AsyncMock)
    async def test_get_streaming_url_spotify(self, mock_spotify, mock_find):
        mock_find.return_value = Platform.SPOTIFY
        mock_spotify.return_value = 'musicinfo'
        result = await music_url_getter.get_streaming_url('url')
        self.assertEqual(result, 'musicinfo')

    @patch('platform_handlers.music_url_getter.find_platform', new_callable=AsyncMock)
    @patch('platform_handlers.music_url_getter.ddl_retrievers.tiktok_ddl_retriever.get_streaming_url', new_callable=AsyncMock)
    async def test_get_streaming_url_tiktok(self, mock_tiktok, mock_find):
        mock_find.return_value = Platform.TIK_TOK
        mock_tiktok.return_value = 'musicinfo'
        result = await music_url_getter.get_streaming_url('url')
        self.assertEqual(result, 'musicinfo')

    @patch('platform_handlers.music_url_getter.find_platform', new_callable=AsyncMock)
    @patch('platform_handlers.music_url_getter.ddl_retrievers.universal_ddl_retriever.get_streaming_url', new_callable=AsyncMock)
    @patch('platform_handlers.music_url_getter.get_audio_content_type', new_callable=AsyncMock)
    async def test_get_streaming_url_anything_else(self, mock_get_audio_type, mock_universal, mock_find):
        mock_find.return_value = Platform.ANYTHING_ELSE
        mock_get_audio_type.return_value = AudioContentType.YT_DLP
        mock_universal.return_value = 'musicinfo'
        result = await music_url_getter.get_streaming_url('url')
        self.assertEqual(result, 'musicinfo')

if __name__ == '__main__':
    unittest.main()
