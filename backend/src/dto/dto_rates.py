from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass(slots=True)
class RatesDTO:
    id: Optional[int] = None
    rate: Optional[float] = None
    amount: Optional[float] = None
    converted_amount: Optional[float] = None
    basecurrencyid: Optional[str] = None
    targetcurrencyid: Optional[str] = None
    basecurrencycode: Optional[str] = None
    targetcurrencycode: Optional[str] = None
    basecurrency: Optional[Dict[str, Any]] = None
    targetcurrency: Optional[Dict[str, Any]] = None

    def to_formatted_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "baseCurrency": self.basecurrency,
            "targetCurrency": self.targetcurrency,
            "rate": self.rate
        }

    def to_formatted_dict_exchange(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "baseCurrency": self.basecurrency,
            "targetCurrency": self.targetcurrency,
            "rate": self.rate,
            "amount": self.amount,
            "convertedAmount": self.converted_amount
        }

