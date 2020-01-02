import abc
import os
from ..return_status import ReturnStatus

class Processor(abc.ABC):
    def __init__(self):
        self.db_processor = None

    @abc.abstractmethod
    def execute(self):
        """ Not implemented - should return pandas dataframe
            that can be written to excel file with df.to_excel
        """
        pass

    def check_input_file(self):
        ret_stat = ReturnStatus()
        if self.db_processor is None:            
            ret_stat.payload["status"] = "error"
            ret_stat.payload["message"] = "Could not find an input file"
            return ret_stat

        input_file = self.db_processor.input_file
        if not os.path.exists(input_file):
            ret_stat.payload["status"] = "error"
            ret_stat.payload["message"] = "Could not find an input file: " + input_file
            return ret_stat
            
        ret_stat.payload["status"] = "success"
        ret_stat.status = True
        return ret_stat




