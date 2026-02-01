class ObjectNotFoundError(Exception):
    def __init__(self, obj: str, field: str | None = None) -> None:
        self.message = f"Объект `{obj}` не найден"
        if field:
            self.message += f" со значением `{field}`"

class Errors():
    def something_goes_wrong():
        return "Что то пошло не так"
       
    

       
    
