import abc
import os
import logging
from ..result import Result

class Processor(abc.ABC):
    def __init__(self):
        self.db_processor = None        
        self.logger = logging.getLogger("LIMS_Run_Processor")

    @abc.abstractmethod
    def execute(self):
        """ Not implemented - should return pandas dataframe
            that can be written to excel file with df.to_excel
        """
        pass

    def log_info(self, message):
        logging.info(message)

    def log_error(self, message):
        logging.error(message)


    def check_input_file(self):
        ret_stat = Result()
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




