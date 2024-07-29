import unittest
from bs4 import BeautifulSoup

from src.utils.col_utils import ColUtils


class TestColUtils(unittest.TestCase):
    def setUp(self):
        self.html_with_link = '<table><tr><td><a href="http://example.com">Example Link</a></td></tr></table>'
        self.html_without_link = '<table><tr><td>No link</td></tr></table>'
        self.html_with_rowspan = '<table><tr><td rowspan="2">Cell with rowspan</td><td>Regular cell</td></tr><tr><td>Another cell</td></tr></table>'
        self.html_without_rowspan = '<table><tr><td>No rowspan</td></tr></table>'
        self.html_with_text = '<table><tr><td>Cell Text</td></tr></table>'

        self.soup_with_link = BeautifulSoup(self.html_with_link, 'html.parser')
        self.soup_without_link = BeautifulSoup(self.html_without_link, 'html.parser')
        self.soup_with_rowspan = BeautifulSoup(self.html_with_rowspan, 'html.parser')
        self.soup_without_rowspan = BeautifulSoup(self.html_without_rowspan, 'html.parser')
        self.soup_with_text = BeautifulSoup(self.html_with_text, 'html.parser')

    def test_extract_col_link(self):
        td = self.soup_with_link.find('td')
        self.assertEqual(ColUtils.extract_col_link(td), 'http://example.com')
        td = self.soup_without_link.find('td')
        self.assertIsNone(ColUtils.extract_col_link(td))

    def test_extract_col_rowspan_number(self):
        td = self.soup_with_rowspan.find('td', rowspan=True)
        self.assertEqual(ColUtils.extract_col_rowspan_number(td), 2)
        td = self.soup_without_rowspan.find('td')
        self.assertEqual(ColUtils.extract_col_rowspan_number(td), 1)

    def test_extract_col_value(self):
        td = self.soup_with_text.find('td')
        self.assertEqual(ColUtils.extract_col_value(td), 'Cell Text')

