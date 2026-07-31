from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class CurrenciesDTO():

    code : str
    fullname : str
    sign : str
    id : Optional[int] = None

    def to_formatted_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.fullname,
            "code": self.code,
            "sign": self.sign
        }