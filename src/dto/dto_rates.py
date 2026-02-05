from dataclasses import dataclass


@dataclass(slots=True)
class RatesDTO():
    
    id : int
    basecurrenceid : str
    targetcurrenceid : str
    rate : int   