from typing import Any

from src.parsers.html_praser import HTMLParserInterface


class TableExtractor:
    """
    TableExtractor is a utility class for extracting tables from an HTML document.
    """

    def __init__(self, parser: HTMLParserInterface) -> None:
        """
        Initialize the TableExtractor with an HTML parser.

        Parameters:
        -----------
        parser : HTMLParserInterface
            An instance of a class that implements the HTMLParserInterface.
        """
        self.parser = parser

    def extract_tables(self) -> Any:
        """
        Extract tables with a specific class from the parsed HTML document.

        Returns:
        --------
        Any
            A list of table elements with the specified class.
        """
        return self.parser.find_all("table", {"class": "wikitable"})
