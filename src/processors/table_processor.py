from dataclasses import dataclass
from typing import List, Set
import re

from config import WORD_SEPERATOR
from src.commons.models.col_details import ColDetails
from src.commons.models.row_details import RowDetails
from src.commons.models.table_details import TableDetails


@dataclass
class TableCellUpdate:
    row_index: int
    col_index: int
    value: str


class TableProcessor:
    @staticmethod
    def insert_values_at_indexes(indexes: List[TableCellUpdate], table: TableDetails) -> TableDetails:
        """
        Inserts values into the table at specified row and column indexes.

        Parameters:
        indexes (List[TableCellUpdate]): A list of TableCellUpdate objects containing row index, column index, and value to be inserted.
        table (TableDetails): The original table details.

        Returns:
        TableDetails: A new TableDetails object with the modified rows.
        """
        updated_rows = []
        for row_index, row in enumerate(table.rows):
            updated_cols = list(row.cols)
            for index in indexes:
                if index.row_index == row_index:
                    updated_cols.insert(index.col_index, ColDetails(value=index.value, link="", rawspans_number=1))
            updated_rows.append(RowDetails(cols=updated_cols))
        return TableDetails(rows=updated_rows, headers=table.headers)

    @staticmethod
    def find_cells_to_update(table: TableDetails) -> List[TableCellUpdate]:
        """
        Finds all cells that need to be updated based on a condition (rawspans_number > 1).

        Parameters:
        table (TableDetails): The original table details.

        Returns:
        List[TableCellUpdate]: A list of TableCellUpdate objects where each contains row index, column index, and cell value.
        """
        indexes = []
        for row_index, row in enumerate(table.rows):
            for col_index, cell in enumerate(row.cols):
                if cell.rawspans_number > 1:
                    indexes.append(TableCellUpdate(row_index + 1, col_index, cell.value))
        return indexes

    @staticmethod
    def get_columns_indexes(table: TableDetails, column_names: List[str]) -> List[int]:
        """
        Gets the indexes of specified column names in the table headers.

        Parameters:
        table (TableDetails): The original table details.
        column_names (List[str]): The column names to find indexes for.

        Returns:
        List[int]: A list of indexes corresponding to the specified column names.
        """
        column_indexes = []
        headers = table.headers
        for index, header in enumerate(headers):
            if header in column_names:
                column_indexes.append(index)
        return column_indexes

    @staticmethod
    def explode_cells(table: TableDetails) -> TableDetails:
        """
        Explodes cells containing '###' into multiple rows.

        Parameters:
        table (TableDetails): The original table details.

        Returns:
        TableDetails: A new TableDetails object with exploded rows.
        """
        exploded_rows: List[RowDetails] = []
        for row in table.rows:
            exploded_rows.extend(TableProcessor.explode_row(row))
        return TableDetails(headers=table.headers, rows=exploded_rows)

    @staticmethod
    def explode_row(row: RowDetails) -> List[RowDetails]:
        """
        Explodes a single row into multiple rows based on '###' in column values.

        Parameters:
        row (RowDetails): The original row details.

        Returns:
        List[RowDetails]: A list of new RowDetails objects with exploded values.
        """
        exploded_rows: List[RowDetails] = []
        new_rows_needed = False
        for col_index, col in enumerate(row.cols):
            if WORD_SEPERATOR in col.value:
                new_rows_needed = True
                exploded_rows.extend(TableProcessor.create_new_rows(row, col_index))
                break
        if not new_rows_needed:
            exploded_rows.append(row.clone())
        return exploded_rows

    @staticmethod
    def create_new_rows(row: RowDetails, col_index: int) -> List[RowDetails]:
        """
        Creates new rows by splitting the column value at '###'.

        Parameters:
        row (RowDetails): The original row details.
        col_index (int): The index of the column to split.

        Returns:
        List[RowDetails]: A list of new RowDetails objects with split values.
        """
        new_rows: List[RowDetails] = []
        for value in row.cols[col_index].value.split(WORD_SEPERATOR):
            new_row = row.clone()
            new_row.cols[col_index].value = value
            new_rows.append(new_row)
        return new_rows

    @staticmethod
    def select_columns_by_indexes(table: TableDetails, column_indexes: List[int]) -> TableDetails:
        """
        Selects specified columns based on their indexes.

        Parameters:
        table (TableDetails): The original table details.
        column_indexes (List[int]): The column indexes to be selected.

        Returns:
        TableDetails: A new TableDetails object with the selected columns.

        Raises:
        IndexError: If any of the column indexes are out of range.
        """
        if not all(0 <= index < len(table.headers) for index in column_indexes):
            raise IndexError("One or more column indexes are out of range")
        sorted_indexes = sorted(column_indexes)
        new_headers = [table.headers[i] for i in sorted_indexes]
        new_rows = [RowDetails(cols=[row.cols[i] for i in sorted_indexes]) for row in table.rows]
        return TableDetails(headers=new_headers, rows=new_rows)

    @staticmethod
    def select_columns_by_names(table: TableDetails, column_names: List[str]) -> TableDetails:
        """
        Selects specified columns by their names and returns a new table with only those columns.

        Parameters:
        table (TableDetails): The original table details.
        column_names (List[str]): The column names to be selected.

        Returns:
        TableDetails: A new TableDetails object with the selected columns.
        """
        column_indexes = TableProcessor.get_columns_indexes(table, column_names)
        updated_table = TableProcessor.select_columns_by_indexes(table, column_indexes)
        return updated_table

    @staticmethod
    def filter_rows_by_column_value(table: TableDetails, column_name: str, pattern: str) -> TableDetails:
        """
        Filters rows based on a regex pattern applied to a specific column.

        Parameters:
        table (TableDetails): The original table details.
        column_name (str): The name of the column to apply the regex pattern.
        pattern (str): The regex pattern to match values against.

        Returns:
        TableDetails: A new TableDetails object with filtered rows.
        """
        column_index = TableProcessor.get_columns_indexes(table, [column_name])[0]
        regex = re.compile(pattern)
        filtered_rows = [
            row for row in table.rows if regex.search(row.cols[column_index].value)
        ]
        return TableDetails(headers=table.headers, rows=filtered_rows)

    @staticmethod
    def get_all_links_by_column(table: TableDetails, column_name: str) -> Set[str]:
        """
        Retrieves all links from a specified column in the table cells.

        Parameters:
        table (TableDetails): The original table details.
        column_name (str): The name of the column to retrieve links from.

        Returns:
        List[str]: A list of links from the specified column in the table cells.
        """
        column_indexes = TableProcessor.get_columns_indexes(table, [column_name])

        if not column_indexes:
            raise ValueError(f"Column '{column_name}' not found in the table headers.")

        column_index = column_indexes[0]
        links = []

        for row in table.rows:
            cell = row.cols[column_index]
            if cell.link:
                links.append(cell.link)

        return links
