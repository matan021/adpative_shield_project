from dataclasses import dataclass


@dataclass
class ColDetails:
    value: str
    link: str
    rawspans_number: int

    def clone(self):
        return ColDetails(self.value, self.link, self.rawspans_number)
