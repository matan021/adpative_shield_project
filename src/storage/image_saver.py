from src.commons.models.image_data import ImageData


class ImageSaver:
    """
    Abstract base class for image saving strategies.
    """

    async def save_image(self, image_data: ImageData) -> None:
        raise NotImplementedError("save_image method not implemented")
