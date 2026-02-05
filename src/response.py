import json
import logging



class Responses():
    def success(data: dict = None):
        respons_data = {
            "data": data,
            "status_code": 200
        }
        return respons_data
    
    def input_err(message: str):
        respons_data = {
            "message": message,
            "status_code": 400
        }
        return respons_data
    
    def not_found_err(message: str):
        respons_data = {
            "message": message,
            "status_code": 404
        }
        return respons_data
    
    def already_exists(message: str):
        respons_data = {
            "message": message,
            "status_code": 409
        }
        return respons_data

    def initial_err(message: str):
        respons_data = {
            "message": message,
            "status_code": 500
        }
        return respons_data