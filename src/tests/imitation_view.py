import os
from dotenv import load_dotenv
import requests


class TestView():
    def __init__(self):
        load_dotenv()
        host, port = os.getenv('SERVER_HOST'), int(os.getenv('SERVER_PORT'))
        self.BASE_URL = f"http://{host}:{port}"

    def do_all_test(self, ):
        data_currencies = {
                            "name": "United States dollar",
                            "code": "USD",
                            "sing": "$"
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

    def post_currencies(self, data):
        return requests.post(f"{self.BASE_URL}/currencies", data=data)

    def get_currency(self, id: int):
        return requests.get('')

    def get_currencies(self, ):
        return requests.get('')
    
    def update_currency(self, id: int, data: dict):
        return requests.post('')
    
    def delete_currency(self, id: int):
        return requests.post('')

    def post_rates(self, data):
        return requests.post(f"{self.BASE_URL}/rates", data=data)

    def get_rate(self, id: int):
        return requests.get('')

    def get_rates(self, ):
        return requests.get('')
    
    def update_rates(self, id: int, data: dict):
        return requests.post('')
    
    def delete_rate(self, id: int):
        return requests.post('')

data_currencies = {
        "name": "United States dollar",
        "code": "USD",
        "sing": "$"
    }
print(TestView().post_currencies(data=data_currencies))
data_rates = {
                        "basecurrenceid" : "USD",
                        "targetcurrenceid" : "RUB",
                        "rate" : 1  
                    }
print(TestView().post_rates(data=data_rates))