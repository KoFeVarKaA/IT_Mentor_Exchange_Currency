class ObjectNotFoundError(Exception):
    def __init__(self, obj: str, field: str | None = None):
        self.message = f"Объект `{obj}` не найден"
        if field:
            self.message += f" со значением `{field}`"

class InitialError():
    def __init__(self):
        self.message = f"Ошибка сервера. Что то пошло не так"