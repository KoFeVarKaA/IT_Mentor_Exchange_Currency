import json
import logging



class Responses():
    def success(message: str = None, data: dict = None):
        respons_data = {}
        if message is not None:
            respons_data["message"] = message
        elif data is not None:
            respons_data["data"] = data
        respons_data["status_code"] = 200
        return json.dumps(respons_data)
    
    def input_err(message: str):
        respons_data = {
            "message": message,
            "status_code": 400
        }
        return json.dumps(respons_data)
    
    def not_found_err(message: str):
        respons_data = {
            "message": message,
            "status_code": 404
        }
        return json.dumps(respons_data)
    
    def initial_err(message: str):
        respons_data = {
            "message": message,
            "status_code": 500
        }
        return json.dumps(respons_data)