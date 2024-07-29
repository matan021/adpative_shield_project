import asyncio
import logging
import os

from src.parsers.beautiful_soup_parser import BeautifulSoupParser
from src.processors.column_builder import BasicBuilder
from src.commons.models.table_details import TableDetails
from src.parsers.header_extractor import BeautifulSoupHeaderExtractor
from src.data_fetchers.image_download_manager import ImageDownloadManager
from src.parsers.row_extractor import RowExtractor
from src.storage.s3_saver import MinioSaver
from src.parsers.table_extractor import TableExtractor
from src.processors.table_processor import TableProcessor
from src.utils.logging_config import setup_logging
from src.utils.url_utils import concat_url
from src.parsers.web_scraper import WebScraper

setup_logging()
logger = logging.getLogger(__name__)


class WorkflowManager:
    def __init__(self, url: str, base_wikipedia: str):
        self.url = url
        self.base_wikipedia = base_wikipedia

    def fetch_data(self):
        try:
            logger.info(f"Fetching data from URL: {self.url}")
            response = WebScraper.fetch_data_from_url(self.url)
            return response
        except Exception as e:
            logger.error(f"Error fetching data from URL: {self.url}: {e}")
            raise

    def parse_html(self, content):
        logger.info("Using BeautifulSoup for HTML parsing")
        parser = BeautifulSoupParser(content)
        return parser

    def process_tables(self, parser):
        try:
            header_extractor = BeautifulSoupHeaderExtractor()
            table_extractor = TableExtractor(parser)
            basic_builder = BasicBuilder()
            row_extractor = RowExtractor(column_builder=basic_builder)

            logger.info("Extracting tables from the parsed HTML")
            tables = table_extractor.extract_tables()

            for table in tables:
                try:
                    logger.info("Extracting rows from the table")
                    row_details = row_extractor.extract_rows_from_table(table)

                    logger.info("Extracting headers from the table")
                    headers = header_extractor.extract_headers_from_table(table)

                    table_details = TableDetails(headers=headers, rows=row_details)

                    logger.info("Finding cells to update in the table details")
                    indexes = TableProcessor.find_cells_to_update(table_details)

                    logger.info("Inserting values at the found indexes")
                    table_details = TableProcessor.insert_values_at_indexes(indexes, table_details)

                    logger.info("Selecting specific columns by names")
                    table_details = TableProcessor.select_columns_by_names(table_details,
                                                                           ["collateral adjective", "animal"])

                    logger.info("Exploding cells in the table details")
                    table_details = TableProcessor.explode_cells(table_details)

                    logger.info("Filtering rows by column value")
                    table_details = TableProcessor.filter_rows_by_column_value(table_details, "collateral adjective",
                                                                               r'^(?!.*[\u0020\u2014]).*$')
                    logger.info(f"Table details after processing: {table_details}")

                    self.download_images(table_details)

                except Exception as e:
                    logger.error(f"Error processing table: {e}")
        except Exception as e:
            logger.error(f"Error during table extraction: {e}")
            raise

    def download_images(self, table_details):
        try:
            logger.info("Getting all links by column 'animal'")
            urls = TableProcessor.get_all_links_by_column(table_details, "animal")
            urls = [concat_url(self.base_wikipedia, path) for path in urls]
            logger.info(f"Concatenated URLs: {urls}")

            logger.info("Using S3Saver to save images")
            s3_saver = MinioSaver(
                minio_url=os.getenv("MINIO_HOST", "localhost:9000"),
                access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
                secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
                bucket_name=os.getenv("MINIO_BUCKET", "images")
            )
            manager = ImageDownloadManager(urls, s3_saver)
            asyncio.run(manager.run())
            logger.info("Image download completed successfully")
        except Exception as e:
            logger.error(f"Error occurred during image download: {e}")

    def run(self):
        try:
            response = self.fetch_data()
            parser = self.parse_html(response.content)
            self.process_tables(parser)
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")

