from datetime import datetime
from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin
from ..result import Result


class NH3_Discrete_Analyzer(Plugin):
    """This is the NH3 Discrete Analyzer data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'nh3_discrete_analyzer'
        self.description = 'Processor for NH3 Discrete Analyzer data files'
        self.version = '1.0'
        self.file_type = ".xls"

    def execute(self, file):
        
        try:
        
            self.input_file = file

            if not self.input_file_exists():
                result = Result("File not found: {}".format(self.input_file), "failure")
                self.logger.error("File not found: {}".format(self.input_file))
                return result
            
            result = Result()
            result.table_name = self.get_base_file_name()

            df = self.get_empty_dataframe()
            wb = self.openpyxl.load_workbook(self.input_file)
            df_xl = self.pd.read_excel(self.input_file)

            #Data is in sheet 1
            sheet = wb.worksheets[0]
            num_rows = sheet.max_row
            num_cols = sheet.max_column                        

            
            analyte_id = "NH3"
            data = list()
            for row_idx in range(2, num_rows + 1):
                row = self.get_template_dict()
                aliquot = sheet.cell(row=row_idx, column=1).value
                if aliquot == None or analyte.strip() == "":
                    break
                aliquot = aliquot.strip()
                items = self.get_aliquot_dilution_factor(aliquot)
                aliquot = items[0]
                dilution_factor =items[1]
                
                measured_val = sheet.cell(row=row_idx, column=2).value
                if measured_val == None or measured_val.strip() == "":
                    measured_val = 0.0

                comment = sheet.cell(row=row_idx, column=5).value
                if comment == None or comment.strip() == "":
                    comment = ""
                comment = comment.strip()

                row["Aliquot"] = aliquot
                row["Analyte Identifier"] = analyte_id
                row["Measured Value"] = measured_val
                row["Comment"] = comment
                row["Dilution Factor"] = dilution_factor
                                
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