from src.dto.dto_currencies import CurrenciesCreateDTO


class CurrenciesCreateSchema():

    id : int
    code : str
    fullname : str
    sing : str

    def to_dto(self) -> CurrenciesCreateDTO:
        return CurrenciesCreateDTO(
            id=self.id,
            code=self.code,
            fullname=self.fullname,
            sing=self.sing
        )
