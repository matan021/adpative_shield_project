import os
from urllib.parse import urlparse
import aiohttp

from src.commons.exceptions.exception import ImageDataLoaderException
from src.commons.models.image_data import ImageData
import logging

logger = logging.getLogger(__name__)


class ImageDataLoader:
    """
    A class to handle loading image data from URLs.
    """

    async def fetch_image_data(self, session: aiohttp.ClientSession, img_url: str) -> ImageData:
        """
        Fetches the image data from a given URL.

        Parameters:
        session (ClientSession): The aiohttp client session.
        img_url (str): The URL of the image to fetch.

        Returns:
        ImageData: The image data encapsulated in an ImageData object.

        Raises:
        ImageDataLoaderException: If there is an error fetching the image data.
        """
        try:
            async with session.get(img_url) as response:
                if response.status == 200:
                    img_name = os.path.basename(urlparse(img_url).path)
                    img_data = await response.read()
                    logger.debug(f"Fetched image {img_name} successfully")
                    return ImageData(name=img_name, data=img_data)
                else:
                    logger.debug(f"Failed to fetch image {img_url}, status code: {response.status}")
                    raise ImageDataLoaderException(f"Failed to fetch image, status code {response.status}", img_url)
        except Exception as e:
            logger.error(f"Failed to fetch image {img_url}: {e}")
            raise ImageDataLoaderException(f"Exception occurred: {e}", img_url)
