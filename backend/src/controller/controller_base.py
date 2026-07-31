from src.utils.exception_handler import ControllerErrorsHandlertype


class BaseController(metaclass=ControllerErrorsHandlertype):
    def do_GET(self):
        pass

    def do_POST(self):
        pass

    def do_PATCH(self):
        pass
