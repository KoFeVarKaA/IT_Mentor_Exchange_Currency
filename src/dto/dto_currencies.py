from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CurrenciesCreateDTO():

    id : int
    code : str
    fullname : str
    sing : str