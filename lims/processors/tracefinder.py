from datetime import datetime
from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin
from ..result import Result

class AliquotAnalyte():
    def __init__(self):
        self.aliquot
        self.analyte_id
        self.measured_value
        self.analysis_datetime
        self.user_defined1


class Tracefinder(Plugin):
    """This is the Tracefinder data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'tracefinder'
        self.description = 'Processor for Tracefinder data files'
        self.file_type = ".xlsx"

    def execute(self, file):
        try:
        
            self.input_file = file

            if not self.input_file_exists():
                result = Result("File not found: {}".format(self.input_file), "failure")
                self.logger.error("File not found: {}".format(self.input_file))
                return result

            aliquot = ""
            result = Result()
            result.table_name = self.get_base_file_name()

            df = self.get_empty_dataframe()
            wb = self.openpyxl.load_workbook(self.input_file)
            #Data is in sheet 2
            sheet = wb.worksheets[1]
            sheets_names = wb.sheetnames
            print(wb.sheetnames)
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            lst_aliquot_analytes = list()

            #Some validation
            sval = sheet.cell(row=8, column=1).value
            sval = sval.strip()
            if sval != "Data File":
                result.status = "failure"
                result.add_message("Did not find expected text 'Data File' on sheet2 cell A8 in file {}".format(self.input_file))
                return result

            #Sheet 2, Row 8, starting at column 2 contains Aliquots 
            for row_idx in range(2, num_rows + 1):

            


        except Exception as e:
            result = Result()
            result.status = "failure"
            result.add_message(str(e))
            print(str(e))
            self.logger.error("Error processing file: {}  Error message: {}".format(self.input_file), str(e))
            return result