from bs4 import Tag
from typing import List

from src.processors.column_builder import ColumnBuilder
from src.commons.models.row_details import RowDetails


class RowExtractor:
    """
    RowExtractor is a utility class for extracting row details from an HTML table.

    Attributes:
    -----------
    column_builder : ColumnBuilderInterface
        An instance of a ColumnBuilderInterface used to build column details.

    Methods:
    --------
    extract_rows_from_table(table: Tag) -> List[RowDetails]:
        Extracts row details from a given <table> tag.

    build_row_details(row: Tag) -> RowDetails:
        Builds RowDetails object from a given <tr> tag.
    """

    def __init__(self, column_builder: ColumnBuilder) -> None:
        """
        Initialize the RowExtractor with a column builder.

        Parameters:
        -----------
        column_builder : ColumnBuilderInterface
            An instance of a ColumnBuilderInterface used to build column details.
        """
        self.column_builder = column_builder

    def extract_rows_from_table(self, table: Tag) -> List[RowDetails]:
        """
        Extract row details from a given HTML <table> tag.

        Parameters:
        -----------
        table : Tag
            A BeautifulSoup Tag object representing a <table> element.

        Returns:
        --------
        List[RowDetails]
            A list of RowDetails objects extracted from the table.
        """
        rows_details = []
        rows = table.find_all("tr")
        for row in rows:
            if row.find("td"):
                rows_details.append(self.build_row_details(row))
        return rows_details

    def build_row_details(self, row: Tag) -> RowDetails:
        """
        Build a RowDetails object from a given HTML <tr> tag.

        Parameters:
        -----------
        row : Tag
            A BeautifulSoup Tag object representing a <tr> element.

        Returns:
        --------
        RowDetails
            An object containing details about the table row.
        """
        cols = row.find_all("td")
        row_details = RowDetails([])
        for col in cols:
            row_details.cols.append(self.column_builder.build(col))
        return row_details
