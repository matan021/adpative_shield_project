from dataclasses import dataclass


@dataclass
class ImageData:
    """
    A dataclass to store image data.
    """
    name: str
    data: bytes
