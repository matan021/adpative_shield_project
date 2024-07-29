from abc import ABC, abstractmethod
from bs4 import Tag
from config import WORD_SEPERATOR
from src.commons.models.col_details import ColDetails
from src.utils.col_utils import ColUtils

class ColumnBuilder(ABC):
    """
    ColumnBuilder is an abstract base class that defines the interface for building ColDetails objects.

    Methods:
    --------
    build(col: Tag) -> ColDetails:
        Abstract method to build and return a ColDetails object from the provided Tag.
    """

    @abstractmethod
    def build(self, col: Tag) -> ColDetails:
        """
        Build a ColDetails object from a BeautifulSoup Tag object.

        Parameters:
        -----------
        col : Tag
            A BeautifulSoup Tag object representing a table column.

        Returns:
        --------
        ColDetails
            An object containing details about the table column, including value, link, and rowspan number.
        """
        pass

class BasicBuilder(ColumnBuilder):
    """
    BasicBuilder is a concrete implementation of the ColumnBuilder abstract base class.
    It constructs a ColDetails object from a BeautifulSoup Tag object.

    Methods:
    --------
    build(col: Tag) -> ColDetails:
        Builds and returns a ColDetails object from the provided Tag.
    """

    def build(self, col: Tag) -> ColDetails:
        """
        Build a ColDetails object from a BeautifulSoup Tag object.

        Parameters:
        -----------
        col : Tag
            A BeautifulSoup Tag object representing a table column.

        Returns:
        --------
        ColDetails
            An object containing details about the table column, including value, link, and rowspan number.
        """
        col_link = ColUtils.extract_col_link(col)
        rawspan = ColUtils.extract_col_rowspan_number(col)
        cleaned_text = self._clean_column_text(col)

        return ColDetails(value=cleaned_text, link=col_link, rawspans_number=rawspan)

    @staticmethod
    def _clean_column_text(col: Tag) -> str:
        """
        Clean and extract text from a BeautifulSoup Tag object, removing <i> tags and handling <br> tags.

        Parameters:
        -----------
        col : Tag
            A BeautifulSoup Tag object representing a table column.

        Returns:
        --------
        str
            Cleaned text extracted from the column.
        """
        # Remove all <i> tags from the column
        for i_tag in col.find_all('i'):
            i_tag.decompose()

        # Extract text from the column, separating by <br> tags
        text = col.get_text(separator='<br>')
        text_list = text.split('<br>')

        # Clean and join the text items
        return WORD_SEPERATOR.join(item.strip() for item in text_list if item.strip())
