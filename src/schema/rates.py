from src.dto.dto_rates import RatesCreateDTO


class RatesCreateSchema():

    id : int
    basecurrenceid : str
    targetcurrenceid : str
    rate : int   

    def to_dto(self) -> RatesCreateDTO:
        return RatesCreateDTO(
            id=self.id,
            basecurrenceid =self.basecurrenceid,
            targetcurrenceid=self.targetcurrenceid,
            rate=self.rate
        )