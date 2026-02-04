from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CurrenciesDTO():

    code : str
    fullname : str
    sing : str
    id : int = None