import unittest
from unittest.mock import MagicMock
from bs4 import BeautifulSoup, Tag
from typing import List

from src.parsers.row_extractor import RowExtractor
from src.processors.column_builder import ColumnBuilder
from src.commons.models.row_details import RowDetails


class TestRowExtractor(unittest.TestCase):

    def setUp(self):
        self.column_builder = MagicMock(ColumnBuilder)
        self.extractor = RowExtractor(self.column_builder)
        self.html = """
        <table>
            <tr><th>Header 1</th><th>Header 2</th></tr>
            <tr><td>Row 1 Col 1</td><td>Row 1 Col 2</td></tr>
            <tr><td>Row 2 Col 1</td><td>Row 2 Col 2</td></tr>
        </table>
        """
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.table = self.soup.find('table')

    def test_extract_rows_from_table(self):
        # Mock the behavior of the column builder
        self.column_builder.build.side_effect = lambda col: col.get_text()

        rows_details = self.extractor.extract_rows_from_table(self.table)

        # Expected row details
        expected_rows = [
            RowDetails(cols=["Row 1 Col 1", "Row 1 Col 2"]),
            RowDetails(cols=["Row 2 Col 1", "Row 2 Col 2"])
        ]

        self.assertEqual(len(rows_details), len(expected_rows))
        for row_detail, expected_row in zip(rows_details, expected_rows):
            self.assertEqual(row_detail.cols, expected_row.cols)

    def test_build_row_details(self):
        row_html = "<tr><td>Row 1 Col 1</td><td>Row 1 Col 2</td></tr>"
        row = BeautifulSoup(row_html, 'html.parser').find('tr')

        # Mock the behavior of the column builder
        self.column_builder.build.side_effect = lambda col: col.get_text()

        row_details = self.extractor.build_row_details(row)

        expected_row_details = RowDetails(cols=["Row 1 Col 1", "Row 1 Col 2"])
        self.assertEqual(row_details.cols, expected_row_details.cols)


if __name__ == '__main__':
    unittest.main()
