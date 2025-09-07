from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CurrenciesCreateDTO():

    id : int = 0
    code : str
    fullname : str
    sing : str