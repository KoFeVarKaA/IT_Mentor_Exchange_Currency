from dataclasses import dataclass


@dataclass(slots=True)
class RatesDTO():
    
    id : int = None
    rate : float = None
    amount : float = None
    converted_amount : float = None
    basecurrencyid : str = None
    targetcurrencyid : str = None
    basecurrencycode : str = None
    targetcurrencycode : str = None
    basecurrency : dict = None
    targetcurrency : dict = None
    

    def to_formatted_dict(self):
        return {
            "id": self.id,
            "baseCurrency": self.basecurrency,
            "targetCurrency": self.targetcurrency,
            "rate": self.rate
        }

    def to_formatted_dict_exchange(self):
        return {
            "id": self.id,
            "baseCurrency": self.basecurrency,
            "targetCurrency": self.targetcurrency,
            "rate": self.rate,
            "amount": self.amount,
            "convertedAmount": self.converted_amount
        }