from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass(slots=True)
class RatesDTO:
    id: int = 0
    rate: float = 0.0
    amount: float = 0.0
    converted_amount: float = 0.0
    basecurrencyid: str = "None"
    targetcurrencyid: str = "None"
    basecurrencycode: str = "None"
    targetcurrencycode: str = "None"
    basecurrency: Dict[str, Any] = field(default_factory=dict)
    targetcurrency: Dict[str, Any] = field(default_factory=dict)

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

