# src/commons/exceptions.py

class ImageDataLoaderException(Exception):
    """Custom exception class for ImageDataLoader errors."""
    def __init__(self, message: str, url: str):
        self.message = message
        self.url = url
        super().__init__(f"{message} (URL: {url})")


class ImageLinkExtractorError(Exception):
    """
    Custom exception class for ImageLinkExtractor errors.
    """
    def __init__(self, message: str, url: str):
        super().__init__(message)
        self.url = url
