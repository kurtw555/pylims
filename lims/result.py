import json
import pandas as pd
from enum import Enum

class Status(Enum):
    FAILURE = 0
    SUCCESS = 1


class Result:
    def __init__(self, message="", status="failure"):        
        #status is success or failure
        self.status = status
        self.payload = dict()
        self.payload["status"] = status
        self.payload["message"] = message
        self.table_name = ""
        self.df = None

    def add_message(self, message):
        self.payload["message"] = message
        

    

    