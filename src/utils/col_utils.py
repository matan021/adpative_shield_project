from bs4 import BeautifulSoup, ResultSet, Tag


class ColUtils:
    @classmethod
    def extract_col_link(cls, col: Tag):
        link = col.find('a')
        return link['href'] if link else None

    @classmethod
    def extract_col_rowspan_number(cls, col: Tag):
        return int(col.get('rowspan', "1"))

    @classmethod
    def extract_col_value(cls, col: Tag) -> str:
        # Extract text value
        return col.get_text(strip=True)

    @classmethod
    def extract_colspan(cls, col: Tag) -> int:
        return int(col.get('colspan', "1"))
