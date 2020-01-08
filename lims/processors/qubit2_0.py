from datetime import datetime
from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin
from ..result import Result


class Qubit2_0(Plugin):
    """This is the Qubit2.0 data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'qubit2_0'
        self.description = 'Processor for Qubit 2.0 data files'
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
            num_rows = sheet.max_row
            num_cols = sheet.max_column

            #The columns in the data file are as follows through column J
            #  A        B          C             D            E       F             G        H          I                   J
            #SED_ID	Name	  Date/Time	  Assay Conc.	Units	Stock Conc.	  Units	  Assay Type   Sample Vol (µL)	 Dilution Factor
            #^^^^^^^   ^^^^^     ^^^^^^^^    ^^^^^^^^^                                                                  ^^^^^^^^^^^^^^^

            #Aliquot  AssayType  Analysis    Measured                                                                   Dilution Factor   
            #ID                  Date/Time   Value

            data = list()
            for row_idx in range(2, num_rows + 1):

                row = self.get_template_dict()

                aliquot = sheet.cell(row=row_idx, column=1).value
                analysis_datetime = sheet.cell(row=row_idx, column=3).value
                measured_val = sheet.cell(row=row_idx, column=4).value
                if measured_val != "":
                    if measured_val == "<0.50":
                        measured_val = "0.0"

                analyte_id = sheet.cell(row=row_idx, column=8).value
                dilution_factor = sheet.cell(row=row_idx, column=10).value

                row["Aliquot"] = aliquot
                row["Analysis Date/Time"] = analysis_datetime
                row["Measured Value"] = measured_val
                row["Analyte Identifier"] = analyte_id
                row["Dilution Factor"] = dilution_factor

                data.append(row)

            df = df.append(data, ignore_index=True)
            result.status = "success"
            result.df = df
            return result



        except Exception as e:
            result = Result()
            result.status = "failure"
            result.add_message(str(e))
            print(str(e))
            self.logger.error("Error processing file: {}  Error message: {}".format(self.input_file), str(e))
            return result


    