from dataclasses import dataclass


@dataclass(slots=True)
class CurrenciesDTO():

    code : str
    fullname : str
    sign : str
    id : int = None

    def to_formatted_dict(self):
        return {
            "id": self.id,
            "name": self.fullname,
            "code": self.code,
            "sign": self.sign
        }