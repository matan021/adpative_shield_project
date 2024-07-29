import unittest
from bs4 import BeautifulSoup

from src.parsers.header_extractor import BeautifulSoupHeaderExtractor


class TestBeautifulSoupHeaderExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = BeautifulSoupHeaderExtractor()
        self.html = """
        <table>
            <tr><th>Header 1</th><th>Header 2</th><th colspan="2">Header 3</th></tr>
            <tr><td>Row 1 Col 1</td><td>Row 1 Col 2</td><td>Row 1 Col 3</td></tr>
            <tr><td>Row 2 Col 1</td><td>Row 2 Col 2</td><td>Row 2 Col 3</td></tr>
        </table>
        """
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.table = self.soup.find('table')

    def test_extract_headers_no_filters(self):
        expected_headers = ['header 1', 'header 2']
        headers = self.extractor.extract_headers_from_table(self.table)
        self.assertEqual(headers, expected_headers)

    def test_extract_headers_with_filters(self):
        self.html = """
        <table>
            <tr><th class="header">Header 1</th><th>Header 2</th><th class="header">Header 3</th></tr>
            <tr><td>Row 1 Col 1</td><td>Row 1 Col 2</td><td>Row 1 Col 3</td></tr>
            <tr><td>Row 2 Col 1</td><td>Row 2 Col 2</td><td>Row 2 Col 3</td></tr>
        </table>
        """
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.table = self.soup.find('table')
        expected_headers = ['header 1', 'header 3']
        headers = self.extractor.extract_headers_from_table(self.table, class_='header')
        self.assertEqual(headers, expected_headers)

    def test_extract_headers_with_id_filter(self):
        self.html = """
        <table>
            <tr><th id="header1">Header 1</th><th id="header2">Header 2</th><th id="header3">Header 3</th></tr>
            <tr><td>Row 1 Col 1</td><td>Row 1 Col 2</td><td>Row 1 Col 3</td></tr>
            <tr><td>Row 2 Col 1</td><td>Row 2 Col 2</td><td>Row 2 Col 3</td></tr>
        </table>
        """
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.table = self.soup.find('table')
        expected_headers = ['header 1']
        headers = self.extractor.extract_headers_from_table(self.table, id='header1')
        self.assertEqual(headers, expected_headers)

    def test_extract_headers_with_colspan(self):
        self.html = """
        <table>
            <tr><th>Header 1</th><th>Header 2</th><th colspan="2">Header 3</th></tr>
            <tr><td>Row 1 Col 1</td><td>Row 1 Col 2</td><td>Row 1 Col 3</td></tr>
            <tr><td>Row 2 Col 1</td><td>Row 2 Col 2</td><td>Row 2 Col 3</td></tr>
        </table>
        """
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.table = self.soup.find('table')
        expected_headers = ['header 1', 'header 2']
        headers = self.extractor.extract_headers_from_table(self.table)
        self.assertEqual(headers, expected_headers)

if __name__ == '__main__':
    unittest.main()
