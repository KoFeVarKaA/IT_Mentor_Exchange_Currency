from src.dto.dto_currencies import CurrenciesDTO


class CurrenciesCreateSchema():

    id : int
    code : str
    fullname : str
    sing : str

    def to_dto(self) -> CurrenciesDTO:
        return CurrenciesDTO(
            id=self.id,
            code=self.code,
            fullname=self.fullname,
            sing=self.sing
        )
