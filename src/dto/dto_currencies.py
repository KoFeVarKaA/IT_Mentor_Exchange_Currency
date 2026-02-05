from dataclasses import dataclass


@dataclass(slots=True)
class CurrenciesDTO():

    code : str
    fullname : str
    sing : str
    id : int = None