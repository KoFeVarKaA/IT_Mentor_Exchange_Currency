from src.service.service_rates import RatesService
from src.controller.controller_base import BaseController


class RateController(BaseController):
    def __init__(
            self,
            service: RatesService,
        ):
        self.service = service