import unittest
from unittest.mock import AsyncMock, patch, MagicMock
import aiohttp
import logging

from src.data_fetchers.image_data_loader import ImageDataLoader
from src.data_fetchers.image_link_extractor import ImageLinkExtractor
from src.storage.image_saver import ImageSaver
from src.data_fetchers.image_download_manager import ImageDownloadManager  # Adjust the import path as needed
from src.commons.models.image_data import ImageData  # Ensure ImageData is imported as a class

logging.basicConfig(level=logging.DEBUG)


class TestImageDownloadManager(unittest.IsolatedAsyncioTestCase):

    async def test_run(self):
        urls = ["http://example.com/page1", "http://example.com/page2"]
        image_urls = ["http://example.com/image1.jpg", "http://example.com/image2.jpeg"]
        image_data = [
            ImageData(name="image1.jpg", data=b"fake_image_data1"),
            ImageData(name="image2.jpeg", data=b"fake_image_data2"),
        ]

        # Create mocks
        mock_load_all_image_links = AsyncMock(return_value=image_urls)
        mock_fetch_image_data = AsyncMock(side_effect=image_data)
        mock_save_image = AsyncMock()

        # Create an instance of the manager
        saver = MagicMock(ImageSaver)
        manager = ImageDownloadManager(urls, saver=saver)

        # Replace the member fields with mocks
        manager._link_extractor.load_all_image_links = mock_load_all_image_links
        manager._data_loader.fetch_image_data = mock_fetch_image_data
        manager._saver.save_image = mock_save_image

        await manager.run()

        mock_load_all_image_links.assert_called_once_with(urls)
        self.assertEqual(mock_fetch_image_data.call_count, len(image_urls))
        self.assertEqual(mock_save_image.call_count, len(image_data))

        for data in image_data:
            mock_save_image.assert_any_call(data)

    async def test_process_image(self):
        img_url = "http://example.com/image1.jpg"
        image_data = ImageData(name="image1.jpg", data=b"fake_image_data")

        # Create mocks
        mock_fetch_image_data = AsyncMock(return_value=image_data)
        mock_save_image = AsyncMock()

        # Create an instance of the manager
        saver = MagicMock(ImageSaver)
        manager = ImageDownloadManager([], saver=saver)

        # Replace the member fields with mocks
        manager._data_loader.fetch_image_data = mock_fetch_image_data
        manager._saver.save_image = mock_save_image

        async with aiohttp.ClientSession() as session:
            await manager.process_image(session, img_url)

        mock_fetch_image_data.assert_called_once_with(session, img_url)
        mock_save_image.assert_called_once_with(image_data)

    async def test_process_image_no_data(self):
        img_url = "http://example.com/image1.jpg"
        image_data = ImageData(name="", data=b"")

        # Create mocks
        mock_fetch_image_data = AsyncMock(return_value=image_data)
        mock_save_image = AsyncMock()

        # Create an instance of the manager
        saver = MagicMock(ImageSaver)
        manager = ImageDownloadManager([], saver=saver)

        # Replace the member fields with mocks
        manager._data_loader.fetch_image_data = mock_fetch_image_data
        manager._saver.save_image = mock_save_image

        async with aiohttp.ClientSession() as session:
            await manager.process_image(session, img_url)

        mock_fetch_image_data.assert_called_once_with(session, img_url)
        mock_save_image.assert_not_called()


if __name__ == '__main__':
    unittest.main()
