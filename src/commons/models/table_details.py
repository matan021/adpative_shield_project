from dataclasses import dataclass
from typing import Sequence, List

from src.commons.models.row_details import RowDetails


@dataclass
class TableDetails:
    headers: Sequence[str]
    rows: List[RowDetails]

    def clone(self):
        new_rows = []
        for row in self.rows:
            new_rows.append(row.clone())

        return TableDetails(headers=self.headers[:], rows=new_rows)

    def __str__(self):
        # Call the print_table method and capture the output as a string
        from io import StringIO
        import sys

        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.print_table()

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        return output

    def print_table(self):
        # Determine column widths based on the headers and the rows
        column_widths = [len(header) for header in self.headers]
        for row in self.rows:
            for col in row.cols:
                column_widths = [
                    max(width, len(col.value))
                    for width in column_widths
                ]

        # Print headers
        header_row = " | ".join(header.ljust(width) for header, width in zip(self.headers, column_widths))
        print(header_row)
        print("-" * len(header_row))  # Print a separator line

        # Print rows
        for row in self.rows:
            row_values = " | ".join(col.value.ljust(width) for col, width in zip(row.cols, column_widths))
            print(row_values)
