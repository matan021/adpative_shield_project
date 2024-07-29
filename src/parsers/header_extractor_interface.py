from abc import ABC, abstractmethod
from typing import List, Any

class HeaderExtractorInterface(ABC):
    """
    HeaderExtractorInterface is an abstract base class for extracting headers from an HTML table.

    Methods:
    --------
    extract_headers_from_table(table: Any, **filters: Any) -> List[str]:
        Abstract method to extract headers from a given <table> tag.
    """

    @abstractmethod
    def extract_headers_from_table(self, table: Any, **filters: Any) -> List[str]:
        """
        Extract headers from a given HTML <table> tag.

        Parameters:
        -----------
        table : Any
            An object representing a <table> element (can be from BeautifulSoup or Scrapy).
        filters : Any
            Optional keyword arguments for filtering <th> elements (e.g., class_, id, etc.).

        Returns:
        --------
        List[str]
            A list of header texts extracted from <th> elements matching the filters.
        """
        pass
