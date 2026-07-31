from typing import Any


class Responses():
    @staticmethod
    def success(data: Any = None, status_code: int = 200):
        respons_data = {
            "data": data,
            "status_code": status_code
        }
        return respons_data
    
    @staticmethod
    def input_err(message: str) -> dict:
        return {
            "data" : {"message": message},
            "status_code": 400
        }
    
    @staticmethod
    def not_found_err(message: str) -> dict:
        return {
            "data" : {"message": message},
            "status_code": 404
        }
    
    @staticmethod
    def already_exists(message: str) -> dict:
        return {
            "data" : {"message": message},
            "status_code": 409
        }

    @staticmethod
    def initial_err(message: str) -> dict:
        return {
            "data" : {"message": message},
            "status_code": 500
        }