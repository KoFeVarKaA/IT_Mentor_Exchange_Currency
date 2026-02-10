from dataclasses import dataclass


@dataclass(slots=True)
class CurrenciesDTO():

    code : str
    fullname : str
    sign : str
    id : int = None