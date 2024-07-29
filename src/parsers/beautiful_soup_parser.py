from bs4 import BeautifulSoup, ResultSet

from src.parsers.html_praser import HTMLParserInterface


class BeautifulSoupParser(HTMLParserInterface):
    """
    BeautifulSoupParser is a concrete implementation of HTMLParserInterface using BeautifulSoup.
    """

    def __init__(self, html_content: str) -> None:
        """
        Initialize the parser with the HTML content.

        Parameters:
        -----------
        html_content : str
            The HTML content to be parsed.
        """
        self.soup = BeautifulSoup(html_content, "html.parser")

    def parse(self, html_content: str) -> BeautifulSoup:
        """
        Parse the HTML content.

        Parameters:
        -----------
        html_content : str
            The HTML content to be parsed.

        Returns:
        --------
        BeautifulSoup
            The parsed HTML document.
        """
        self.soup = BeautifulSoup(html_content, "html.parser")
        return self.soup

    def find_all(self, tag: str, attributes: dict = None) -> ResultSet:
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
        ResultSet
            A ResultSet of matching tags.
        """
        return self.soup.find_all(tag, attributes)
