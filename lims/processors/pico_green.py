from datetime import datetime
from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin
from ..result import Result


class PicoGreen(Plugin):
    """This is the Pico Green data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'pico_green'
        self.description = 'Processor for PicoGreen data files'
        self.file_type = ".xlsx"

    def execute(self, file):
        
        try:

            analyte_id = "dsDNA"
            self.input_file = file
            result = None
            if not self.input_file_exists():
                result = Result("File not found: {}".format(self.input_file), "failure")
                self.logger.error("File not found: {}".format(self.input_file))
                return result

            aliquot = ""          
            result = Result()  
            result.table_name = self.get_base_file_name()

            df = self.get_empty_dataframe()
            wb = self.openpyxl.load_workbook(self.input_file)
            sheet = wb.worksheets[0]
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            well_id = sheet.cell(row=18, column=1).value
            well_id = well_id.strip()
            if well_id != "Well ID":
                result = Result("Missing expected data in Row 18, Column 1. Should be Well ID.  File: {}".format(self.input_file), "failure")
                return result

            #              Row 18 starts the data
            #Data File||     Well ID	Name	 Well	      485/20,528/20	  [Concentration]
            #Template ||                Aliquot  Description                  Measured Value      

            #Analyte Identifier is dsDNA for every record
            for row_idx in range(19, num_rows + 1):
                row = self.get_template_dict()

                aliquot = sheet.cell(row=row_idx, column=2).value
                desc = sheet.cell(row=row_idx, column=3).value
                measured_val = sheet.cell(row=row_idx, column=5).value

                row["Aliquot"] = aliquot
                row["Description"] = desc
                row["Measured Value"] = measured_val
                row["Analyte Identifier"] = analyte_id

                df = df.append(row, ignore_index=True)
            
            result.status = "success"
            result.df = df
            
            return result

        except Exception as e:
            result.status = "failure"
            result.add_message(str(e))
            print(str(e))
            self.logger.error("Error processing file: {}  Error message: {}".format(self.input_file), str(e))
            return result