import logging

from minio import Minio
from minio.error import S3Error
import io
from src.commons.models.image_data import ImageData
from src.storage.image_saver import ImageSaver

logger = logging.getLogger(__name__)

class MinioSaver(ImageSaver):
    """
    A class to save images to a MinIO bucket.
    """

    def __init__(self, bucket_name: str, minio_url: str, access_key: str, secret_key: str):
        """
        Initializes the MinioSaver with the specified bucket and MinIO credentials.

        Parameters:
        bucket_name (str): The name of the MinIO bucket.
        minio_url (str): The MinIO server URL.
        access_key (str): The MinIO access key.
        secret_key (str): The MinIO secret key.
        """
        self.bucket_name = bucket_name
        self.minio_client = Minio(minio_url, access_key=access_key, secret_key=secret_key, secure=False)

        # Create the bucket if it does not exist
        if not self.minio_client.bucket_exists(bucket_name):
            self.minio_client.make_bucket(bucket_name)
        else:
            logger.info(f"Bucket '{bucket_name}' already exists")

    async def save_image(self, image_data: ImageData) -> None:
        """
        Saves a single image to the specified MinIO bucket.

        Parameters:
        image_data (ImageData): The image data to save.
        """
        try:
            # Convert the bytes object to a BytesIO stream
            data_stream = io.BytesIO(image_data.data)

            # Upload the image to MinIO
            self.minio_client.put_object(
                self.bucket_name,
                image_data.name,
                data_stream,
                length=len(image_data.data),
                content_type="application/octet-stream"  # Specify content type if needed
            )
            logger.info(f"Uploaded {image_data.name} to MinIO bucket {self.bucket_name}")
        except S3Error as e:
            logger.error(f"Failed to upload {image_data.name} to MinIO: {e}")
