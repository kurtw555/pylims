from datetime import datetime
from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin
from ..result import Result


class MiSeq_18S(Plugin):
    """This is the MiSeq-18S data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'miseq_18s'
        self.description = 'Processor for MiSeq-18S data files'
        self.version = '1.0'
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
            #Data is in sheet 1
            sheet = wb.worksheets[0]
            num_rows = sheet.max_row
            num_cols = sheet.max_column                        

            #Build list of analyte ids
            lst_analytes = list()
            lst_descriptions = list()
            for row_idx in range(2, num_rows + 1):                
                analyte = sheet.cell(row=row_idx, column=1).value
                if analyte == None or analyte.strip() == "":
                    break
                analyte = analyte.strip()
                lst_analytes.append(analyte)

                desc = sheet.cell(row=row_idx, column=2).value
                if desc == None:
                    desc = ""
                else:
                    desc = desc.split()
                lst_descriptions.append(desc)

                
            #Get description row range
            for row_idx in range(2, len(lst_analytes) +2):
                analyte = lst_analytes[row_idx - 2]
                desc = lst_descriptions[row_idx - 2]

                for col_idx in range(2, num_cols ):
                    row = self.get_template_dict()
                    
                    row["Analyte Identifier"] = analyte
                    row["Description"] = desc

                    aliquot = sheet.cell(row=1, column=col_idx).value
                    if aliquot == None:
                        aliquot = ""
                    row["Aliquot"] = aliquot


                    cell_val = sheet.cell(row=row_idx, column=col_idx).value
                    measured_val = 0
                    if cell_val is None or self.is_number(measured_val):
                        measured_val = 0

                    row["Measured Value"] = measured_val
                    data.append(row)
                
            df = df.append(data, ignore_index=True)
            result.status = "success"
            result.df = df


        except Exception as e:
            result = Result()
            result.status = "failure"
            result.add_message(str(e))
            print(str(e))
            self.logger.error("Error processing file: {}  Error message: {}".format(self.input_file), str(e))
            return result