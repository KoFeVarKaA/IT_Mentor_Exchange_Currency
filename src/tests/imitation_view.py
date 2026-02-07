import os
import pytest
import requests
from dotenv import load_dotenv

class TestCurrencyAPI:
    @classmethod
    def setup_class(cls):
        load_dotenv()
        host, port = os.getenv('SERVER_HOST'), int(os.getenv('SERVER_PORT'))
        cls.BASE_URL = f"http://{host}:{port}"
        cls._add_test_currencies()
        cls._add_test_exchange_rates()

    @classmethod
    def _add_test_currencies(cls):
        currencies = [
            {"name": "United States dollar", 
             "code": "USD", 
             "sign": "$"},

            {"name": "Euro", 
             "code": "EUR", 
             "sign": "€"},

            {"name": "Russian Ruble", 
             "code": "RUB", 
             "sign": "₽"},
        ]
        for currency in currencies:
            response = requests.post(f"{cls.BASE_URL}/currencies", data=currency)
            assert response.status_code == 201

    @classmethod
    def _add_test_exchange_rates(cls):
        rates = [
            {"baseCurrencyCode": "USD", "targetCurrencyCode": "EUR", "rate": 0.99},
            {"baseCurrencyCode": "USD", "targetCurrencyCode": "RUB", "rate": 90.0},
        ]
        for rate in rates:
            response = requests.post(f"{cls.BASE_URL}/exchangeRates", data=rate)
            assert response.status_code == 201

    
    # Тесты для валют
    def test_get_currencies_success(self):
        response = requests.get(f"{self.BASE_URL}/currencies")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_currency_success(self):
        response = requests.get(f"{self.BASE_URL}/currency/USD")
        assert response.status_code == 200
        assert response.json()["code"] == "USD"

    def test_get_currency_not_found(self):
        response = requests.get(f"{self.BASE_URL}/currency/XXX")
        assert response.status_code == 404

    def test_get_currency_bad_request(self):
        response = requests.get(f"{self.BASE_URL}/currency/")
        assert response.status_code == 400

    def test_post_currency_success(self):
        data = {
            "name": "Test Currency",
            "code": "TST",
            "sign": "₸"
        }
        response = requests.post(f"{self.BASE_URL}/currencies", data=data)
        assert response.status_code == 201
        assert response.json()["code"] == "TST"

    def test_post_currency_missing_field(self):
        data = {
            "name": "Test Currency",
            "sign": "₸"
        }
        response = requests.post(f"{self.BASE_URL}/currencies", data=data)
        assert response.status_code == 400

    def test_post_currency_conflict(self):
        data = {
            "name": "Test Currency",
            "code": "USD",  # Уже существует
            "sign": "$"
        }
        response = requests.post(f"{self.BASE_URL}/currencies", data=data)
        assert response.status_code == 409

    # Тесты для обменных курсов
    def test_get_exchange_rates_success(self):
        response = requests.get(f"{self.BASE_URL}/exchangeRates")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_exchange_rate_success(self):
        response = requests.get(f"{self.BASE_URL}/exchangeRate/USDRUB")
        assert response.status_code == 200
        assert response.json()["baseCurrency"]["code"] == "USD"
        assert response.json()["targetCurrency"]["code"] == "RUB"

    def test_get_exchange_rate_not_found(self):
        response = requests.get(f"{self.BASE_URL}/exchangeRate/USDXYY")
        assert response.status_code == 404

    def test_get_exchange_rate_bad_request(self):
        response = requests.get(f"{self.BASE_URL}/exchangeRate/")
        assert response.status_code == 400

    def test_post_exchange_rate_success(self):
        data = {
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "TST",
            "rate": 1.5
        }
        response = requests.post(f"{self.BASE_URL}/exchangeRates", data=data)
        assert response.status_code == 201
        assert response.json()["baseCurrency"]["code"] == "USD"
        assert response.json()["targetCurrency"]["code"] == "TST"

    def test_post_exchange_rate_missing_field(self):
        data = {
            "baseCurrencyCode": "USD",
            "rate": 1.5
        }
        response = requests.post(f"{self.BASE_URL}/exchangeRates", data=data)
        assert response.status_code == 400

    def test_post_exchange_rate_currency_not_found(self):
        data = {
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "XXX",  # Несуществующая валюта
            "rate": 1.5
        }
        response = requests.post(f"{self.BASE_URL}/exchangeRates", data=data)
        assert response.status_code == 404

    def test_post_exchange_rate_conflict(self):
        data = {
            "baseCurrencyCode": "USD",
            "targetCurrencyCode": "RUB",  # Уже существует
            "rate": 1.5
        }
        response = requests.post(f"{self.BASE_URL}/exchangeRates", data=data)
        assert response.status_code == 409

    def test_patch_exchange_rate_success(self):
        data = {"rate": 2.0}
        response = requests.patch(f"{self.BASE_URL}/exchangeRate/USDTST", data=data)
        assert response.status_code == 200
        assert response.json()["rate"] == 2.0

    def test_patch_exchange_rate_not_found(self):
        data = {"rate": 2.0}
        response = requests.patch(f"{self.BASE_URL}/exchangeRate/USDXYY", data=data)
        assert response.status_code == 404

    def test_patch_exchange_rate_missing_field(self):
        data = {}
        response = requests.patch(f"{self.BASE_URL}/exchangeRate/USDTST", data=data)
        assert response.status_code == 400

    #  Тесты для обмена валюты
    def test_exchange_success_direct(self):
        response = requests.get(f"{self.BASE_URL}/exchange?from=USD&to=TST&amount=10")
        assert response.status_code == 200
        assert response.json()["convertedAmount"] == 20.0  # 10 * 2.0

    def test_exchange_success_reverse(self):
        response = requests.get(f"{self.BASE_URL}/exchange?from=TST&to=USD&amount=15")
        assert response.status_code == 200
        assert response.json()["convertedAmount"] == 7.5  # 15 / 0.5

    def test_exchange_success_via_usd(self):
        response = requests.get(f"{self.BASE_URL}/exchange?from=EUR&to=TST&amount=10")
        assert response.status_code == 200
        assert "convertedAmount" in response.json()

    def test_exchange_currency_not_found(self):
        response = requests.get(f"{self.BASE_URL}/exchange?from=XXX&to=TST&amount=10")
        assert response.status_code == 404