import asyncio
from typing import List
import aiohttp
import logging

from src.data_fetchers.image_data_loader import ImageDataLoader
from src.data_fetchers.image_link_extractor import ImageLinkExtractor
from src.storage.image_saver import ImageSaver

logger = logging.getLogger(__name__)


class ImageDownloadManager:
    """
    A class to manage the process of extracting image links, loading image data, and saving images.
    """

    def __init__(self, urls: List[str], saver: ImageSaver, max_concurrent_requests: int = 100):
        """
        Initializes the ImageDownloadManager with the URLs, saving strategy, and concurrency settings.

        Parameters:
        urls (List[str]): The list of URLs to process.
        saver (ImageSaver): The saving strategy to use (FileSystemSaver or S3Saver).
        max_concurrent_requests (int): Maximum number of concurrent requests.
        """
        self.urls = urls
        self._link_extractor = ImageLinkExtractor(max_concurrent_requests)
        self._data_loader = ImageDataLoader()
        self._saver = saver

    async def run(self) -> None:
        """
        Runs the process to get image links, load image data, and save images using the specified strategy.
        """
        image_links = await self._link_extractor.load_all_image_links(self.urls)
        connector = aiohttp.TCPConnector(limit_per_host=10)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.process_image(session, img_url) for img_url in image_links]
            await asyncio.gather(*tasks)

    async def process_image(self, session: aiohttp.ClientSession, img_url: str) -> None:
        """
        Processes an image by loading its data and saving it using the specified strategy.

        Parameters:
        session (ClientSession): The aiohttp client session.
        img_url (str): The URL of the image to process.
        """
        logger.debug(f"Processing image: {img_url}")
        image_data = await self._data_loader.fetch_image_data(session, img_url)
        if image_data.name and image_data.data:
            logger.debug(f"Saving image: {image_data.name}")
            await self._saver.save_image(image_data)
        else:
            logger.debug(f"Skipping empty image: {img_url}")
