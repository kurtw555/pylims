import json

class ReturnStatus:
    def __init__(self, message="", status=""):
        self.status = False
        self.payload = dict()
        self.payload["status"] = status
        self.payload["message"] = message

        

    

    