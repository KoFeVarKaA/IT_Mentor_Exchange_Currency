from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RatesCreateDTO():
    
    id : int
    basecurrenceid : str
    targetcurrenceid : str
    rate : int   