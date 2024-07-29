import logging
import os
from src.commons.models.image_data import ImageData
from src.storage.image_saver import ImageSaver

logger = logging.getLogger(__name__)


class FileSystemSaver(ImageSaver):
    """
    A class to save images to the local file system.
    """

    def __init__(self, download_folder: str):
        """
        Initializes the FileSystemSaver with the specified download folder.

        Parameters:
        download_folder (str): The folder to save the downloaded images.
        """
        self.download_folder = download_folder
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

    async def save_image(self, image_data: ImageData) -> None:
        """
        Saves a single image to the local file system.

        Parameters:
        image_data (ImageData): The image data to save.
        """
        try:
            img_path = os.path.join(self.download_folder, image_data.name)
            with open(img_path, 'wb') as img_file:
                img_file.write(image_data.data)
            logger.info(f"Downloaded {image_data.name} to {img_path}")
        except Exception as e:
            logger.error(f"Failed to save image {image_data.name}: {e}")
