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

    def post_rates(self, data):
        return requests.post(f"{self.BASE_URL}/exchangeRates", data=data)
    
    def patch_rate(self, path, data):
        return requests.patch(f"{self.BASE_URL}//exchangeRate/{path}", data=data)

view = TestView()

data_currencies = {
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    }
data_currencies2 = {
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    }
# print(view.post_currencies(data=data_currencies))
# print(view.post_currencies(data=data_currencies2))
data_rates = {
                        "baseCurrencyCode" : "USD",
                        "targetCurrencyCode" : "EUR",
                        "rate" : 1.5 
                    }
data_patch = {
        "rate" : 1.4,
}
# print(view.post_rates(data=data_rates))
print(view.patch_rate(path="USDEUR", data=data_patch))