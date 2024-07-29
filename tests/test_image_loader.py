import unittest
from unittest.mock import patch
import aiohttp
from aioresponses import aioresponses

from src.commons.models.image_data import ImageData
from src.data_fetchers.image_data_loader import ImageDataLoader


class TestImageDataLoader(unittest.IsolatedAsyncioTestCase):

    @patch('builtins.print')  # Mock the print function to suppress output in tests
    async def test_fetch_image_data_success(self, mock_print):
        loader = ImageDataLoader()
        img_url = "http://example.com/test.jpg"
        img_name = "test.jpg"
        img_data = b"fake_image_data"

        with aioresponses() as m:
            m.get(img_url, status=200, body=img_data)
            async with aiohttp.ClientSession() as session:
                image_data = await loader.fetch_image_data(session, img_url)

                self.assertEqual(image_data.name, img_name)
                self.assertEqual(image_data.data, img_data)

    @patch('builtins.print')  # Mock the print function to suppress output in tests
    async def test_fetch_image_data_failure(self, mock_print):
        loader = ImageDataLoader()
        img_url = "http://example.com/test.jpg"

        with aioresponses() as m:
            m.get(img_url, status=404)
            async with aiohttp.ClientSession() as session:
                image_data = await loader.fetch_image_data(session, img_url)

                self.assertEqual(image_data.name, "")
                self.assertEqual(image_data.data, b"")

    @patch('builtins.print')  # Mock the print function to suppress output in tests
    async def test_fetch_image_data_exception(self, mock_print):
        loader = ImageDataLoader()
        img_url = "http://example.com/test.jpg"

        with patch.object(aiohttp.ClientSession, 'get', side_effect=Exception("Test exception")):
            async with aiohttp.ClientSession() as session:
                image_data = await loader.fetch_image_data(session, img_url)

                self.assertEqual(image_data.name, "")
                self.assertEqual(image_data.data, b"")

if __name__ == '__main__':
    unittest.main()
