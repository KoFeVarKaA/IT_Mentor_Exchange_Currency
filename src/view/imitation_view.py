import requests

from schema.currencies import CurrenciesCreateSchema


class TestView():
    def do_all_test():
        data_currencies = {
                            "name": "United States dollar",
                            "code": "USD",
                            "sign": "$"
                        }
        data_currency_update = {}

        data_rates = {
                        "basecurrenceid" : "USD",
                        "targetcurrenceid" : "RUB",
                        "rate" : 1  
                    }
        data_rate_update = {}
        
        responses = [
            TestView.post_currencies(data_currencies),
            TestView.post_rates(data_rates),

            TestView.get_currency(id=1),
            TestView.get_currencies(),
            TestView.get_rate(id=1),
            TestView.get_rates(),

            TestView.update_currency(1, data_currency_update),
            TestView.update_rates(1, data_rate_update),
            TestView.get_currencies(),
            TestView.get_rates(),

            TestView.delete_currency(id=1),
            TestView.delete_rate(id=1),
        ]
        return responses

    def post_currencies(data):
        return requests.post('')

    def get_currency(id: int):
        return requests.get('')

    def get_currencies() -> list[CurrenciesCreateSchema]:
        return requests.get('')
    
    def update_currency(id: int, data: dict):
        return requests.post('')
    
    def delete_currency(id: int):
        return requests.post('')

    
    def post_rates(datad):
        return requests.post('')

    def get_rate(id: int):
        return requests.get('')

    def get_rates():
        return requests.get('')
    
    def update_rates(id: int, data: dict):
        return requests.post('')
    
    def delete_rate(id: int):
        return requests.post('')
