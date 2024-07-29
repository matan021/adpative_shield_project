import asyncio
import logging
from typing import List
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from src.commons.exceptions.exception import ImageLinkExtractorError

logger = logging.getLogger(__name__)


class ImageLinkExtractor:
    """
    A class to handle fetching and extracting image links from webpages.
    """

    def __init__(self, max_concurrent_requests: int = 100):
        """
        Initializes the ImageLinkExtractor with the specified maximum number of concurrent requests.

        Parameters:
        max_concurrent_requests (int): Maximum number of concurrent requests.
        """
        self.max_concurrent_requests = max_concurrent_requests

    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> str:
        """
        Fetches the content of the URL asynchronously.

        Parameters:
        session (ClientSession): The aiohttp client session.
        url (str): The URL to fetch.

        Returns:
        str: The HTML content of the page.

        Raises:
        ImageLinkExtractorError: If the page fetch fails.
        """
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            logger.error(f"Failed to fetch {url}: {e}")
            raise ImageLinkExtractorError(f"Failed to fetch {url}", url) from e

    async def extract_image_links(self, session: aiohttp.ClientSession, url: str) -> List[str]:
        """
        Extracts image links (only .jpg or .jpeg) from a given webpage.

        Parameters:
        session (ClientSession): The aiohttp client session.
        url (str): The URL of the webpage to extract images from.

        Returns:
        List[str]: A list of image URLs.

        Raises:
        ImageLinkExtractorError: If no image links are found on the page.
        """
        try:
            html_content = await self.fetch_page(session, url)
            soup = BeautifulSoup(html_content, 'html.parser')
            image_tags = soup.find_all('img')
            image_links = []

            for img in image_tags:
                img_url = img.get('src')
                if img_url and (img_url.endswith('.jpg') or img_url.endswith('.jpeg')):
                    img_url = urljoin(url, img_url)  # Handle relative URLs
                    image_links.append(img_url)

            if not image_links:
                raise ImageLinkExtractorError(f"No image links found at {url}", url)

            return image_links
        except ImageLinkExtractorError as e:
            logger.error(f"Error extracting image links from {url}: {e}")
            raise

    async def load_all_image_links(self, urls: List[str]) -> List[str]:
        """
        Loads image links from a list of URLs.

        Parameters:
        urls (List[str]): The list of URLs to process.

        Returns:
        List[str]: A list of all image URLs extracted from the given URLs.
        """
        connector = aiohttp.TCPConnector(limit=self.max_concurrent_requests)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [self.extract_image_links(session, url) for url in urls]
            try:
                image_links_list = await asyncio.gather(*tasks)
            except ImageLinkExtractorError:
                # If an error occurs, it will be logged by the individual methods
                return []
            image_links = [img_url for sublist in image_links_list for img_url in sublist]
            return image_links
