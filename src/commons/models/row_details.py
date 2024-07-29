from dataclasses import dataclass
from typing import List

from src.commons.models.col_details import ColDetails


@dataclass
class RowDetails:
    cols: List[ColDetails]

    def clone(self):
        new_cols = []
        for col in self.cols:
            new_cols.append(col.clone())

        return RowDetails(new_cols)
