from dataclasses import dataclass


@dataclass(slots=True)
class RatesDTO():
    
    rate : int = None
    basecurrenceid : str = None
    targetcurrenceid : str = None
    basecurrencecode : str = None
    targetcurrencecode : str = None
    basecurrence : dict = None
    targetcurrence : dict = None
    id : int = None