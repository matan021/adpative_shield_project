from bs4 import Tag
from typing import List, Any

from src.parsers.header_extractor_interface import HeaderExtractorInterface


class BeautifulSoupHeaderExtractor(HeaderExtractorInterface):
    """
    BeautifulSoupHeaderExtractor is a concrete implementation of the HeaderExtractorInterface.
    It extracts headers from an HTML table using BeautifulSoup.

    Methods:
    --------
    extract_headers_from_table(table: Tag, **filters: Any) -> List[str]:
        Extracts headers from a given <table> tag, optionally filtering <th> elements based on given attributes.
    """

    def extract_headers_from_table(self, table: Tag, **filters: Any) -> List[str]:
        """
        Extract headers from a given HTML <table> tag.

        Parameters:
        -----------
        table : Tag
            A BeautifulSoup Tag object representing a <table> element.
        filters : Any
            Optional keyword arguments for filtering <th> elements (e.g., class_, id, etc.).

        Returns:
        --------
        List[str]
            A list of header texts extracted from <th> elements matching the filters.
        """
        headers = table.find_all('th', **filters)
        headers = [header for header in headers if header.get("colspan") is None]
        return [header.get_text(strip=True).lower() for header in headers]
