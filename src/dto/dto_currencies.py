from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CurrenciesCreateDTO():

    code : str
    fullname : str
    sing : str
    id : int = 0