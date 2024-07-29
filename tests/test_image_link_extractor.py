import unittest
from unittest.mock import patch
import aiohttp
from aioresponses import aioresponses
import asyncio

from src.data_fetchers.image_link_extractor import ImageLinkExtractor


class TestImageLinkExtractor(unittest.IsolatedAsyncioTestCase):

    @patch('builtins.print')  # Mock the print function to suppress output in tests
    async def test_fetch_page_success(self, mock_print):
        extractor = ImageLinkExtractor()
        url = "http://example.com/test.html"
        html_content = "<html><body><h1>Test Page</h1></body></html>"

        with aioresponses() as m:
            m.get(url, status=200, body=html_content)
            async with aiohttp.ClientSession() as session:
                fetched_content = await extractor.fetch_page(session, url)
                self.assertEqual(fetched_content, html_content)

    @patch('builtins.print')  # Mock the print function to suppress output in tests
    async def test_fetch_page_failure(self, mock_print):
        extractor = ImageLinkExtractor()
        url = "http://example.com/test.html"

        with aioresponses() as m:
            m.get(url, status=404)
            async with aiohttp.ClientSession() as session:
                fetched_content = await extractor.fetch_page(session, url)
                self.assertEqual(fetched_content, "")

    @patch('builtins.print')  # Mock the print function to suppress output in tests
    async def test_extract_image_links(self, mock_print):
        extractor = ImageLinkExtractor()
        url = "http://example.com/test.html"
        html_content = """
            <html>
            <body>
                <img src="image1.jpg"/>
                <img src="image2.jpeg"/>
                <img src="image3.png"/>
            </body>
            </html>
        """
        expected_image_links = ["http://example.com/image1.jpg", "http://example.com/image2.jpeg"]

        with aioresponses() as m:
            m.get(url, status=200, body=html_content)
            async with aiohttp.ClientSession() as session:
                image_links = await extractor.extract_image_links(session, url)
                self.assertEqual(image_links, expected_image_links)

    @patch('builtins.print')  # Mock the print function to suppress output in tests
    async def test_load_all_image_links(self, mock_print):
        extractor = ImageLinkExtractor()
        urls = ["http://example.com/test1.html", "http://example.com/test2.html"]
        html_content1 = """
            <html>
            <body>
                <img src="image1.jpg"/>
            </body>
            </html>
        """
        html_content2 = """
            <html>
            <body>
                <img src="image2.jpeg"/>
            </body>
            </html>
        """
        expected_image_links = ["http://example.com/image1.jpg", "http://example.com/image2.jpeg"]

        with aioresponses() as m:
            m.get(urls[0], status=200, body=html_content1)
            m.get(urls[1], status=200, body=html_content2)
            image_links = await extractor.load_all_image_links(urls)
            self.assertEqual(image_links, expected_image_links)

if __name__ == '__main__':
    unittest.main()
