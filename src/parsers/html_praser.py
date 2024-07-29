from abc import ABC, abstractmethod
from typing import Any

class HTMLParserInterface(ABC):
    """
    HTMLParserInterface is an abstract base class for HTML parsers.
    """

    @abstractmethod
    def parse(self, html_content: str) -> Any:
        """
        Parse the HTML content.

        Parameters:
        -----------
        html_content : str
            The HTML content to be parsed.

        Returns:
        --------
        Any
            The parsed HTML document.
        """
        pass

    @abstractmethod
    def find_all(self, tag: str, attributes: dict = None) -> Any:
        """
        Find all tags in the parsed HTML document that match the given criteria.

        Parameters:
        -----------
        tag : str
            The name of the tag to find.
        attributes : dict, optional
            A dictionary of tag attributes to match.

        Returns:
        --------
        Any
            A list of matching tags.
        """
        pass
