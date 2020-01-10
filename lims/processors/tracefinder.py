from datetime import datetime
from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin
from ..result import Result

class AliquotAnalyte():
    def __init__(self, aliquot, analyte_id, measured_val="", analysis_datetime="", user_defined1=""):
        self.aliquot = aliquot
        self.analyte_id = analyte_id
        self.measured_value = measured_val
        self.analysis_datetime = analysis_datetime
        self.user_defined1 = user_defined1


class Tracefinder(Plugin):
    """This is the Tracefinder data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'tracefinder'
        self.description = 'Processor for Tracefinder data files'
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
            #Data is in sheet 2
            sheet = wb.worksheets[1]
            sheets_names = wb.sheetnames
            print(wb.sheetnames)
            num_rows = sheet.max_row
            num_cols = sheet.max_column            

            #Some validation
            sval = sheet.cell(row=8, column=1).value
            sval = sval.strip()
            if sval != "Data File":
                result.status = "failure"
                result.add_message("Did not find expected text 'Data File' on sheet2 cell A8 in file {}".format(self.input_file))
                return result

            lst_aliquot_analytes = list()
            lst_analyte_ids = list()            
            #Sheet 2, Row 8, starting at column 2 contains Analytes IDs 
            for col_idx in range(2, num_cols + 1):
                cell_val = sheet.cell(row=8, column=col_idx).value
                cell_val = cell_val.strip()
                if cell_val != "All Flags":
                    lst_analyte_ids.append(cell_val)
                else:                    
                    break

            analyze_date = sheet.cell(row=8, column=num_cols).value
            analyze_date = analyze_date.strip()
            if analyze_date != "Sample Acquisition Date":
                result.status = "failure"
                result.add_message("Sample Acquisition Date not in correct location: Row {0}, Column {1}. File: {2}".format(self.input_file, 8, num_cols))
                return result

            #Sheet 2, Row 9 down, Column 1 contains Aliquot name
            #Sheet 2, Row 9 down, Column 2 until 'All Flags' contain data
            for row_idx in range(9, num_rows + 1):
                aliquot = sheet.cell(row=row_idx, column=1).value
                analysis_datetime = sheet.cell(row=row_idx, column=num_cols).value

                for col_idx in range(2, len(lst_analyte_ids) + 2):
                    
                    analyte_id = lst_analyte_ids[col_idx - 2]
                    measured_val = sheet.cell(row=row_idx, column=col_idx).value

                    aliquot_analyte = AliquotAnalyte(aliquot,analyte_id,measured_val,analysis_datetime)
                    lst_aliquot_analytes.append(aliquot_analyte)

            #End   processing of sheet 2--------------------------------------------------------------------


            #Start processing of sheet 4--------------------------------------------------------------------
            sheet = wb.worksheets[3]
            num_rows = sheet.max_row
            num_cols = sheet.max_column
            #Sheet 4, Row 8, starting at column 2 contains Aliquots 
            lst_analyte_ids = list()
            for col_idx in range(2, num_cols + 1):
                cell_val = sheet.cell(row=8, column=col_idx).value
                cell_val = cell_val.strip()
                if cell_val != "All Flags":
                    lst_analyte_ids.append(cell_val)
                else:                    
                    break

            #Sheet 4, Row 9 down, Column 1 contains Aliquot name
            #Sheet 4, Row 9 down, Column 2 until 'All Flags' contain data
            for row_idx in range(9, num_rows + 1):
                aliquot = sheet.cell(row=row_idx, column=1).value

                #Sheet 4, Row 9 down, Column 1 contains Aliquot name
                for col_idx in range(2, len(lst_analyte_ids) + 2):
                    analyte = lst_analyte_ids[col_idx-2]

                    al = [x for x in lst_aliquot_analytes if x.aliquot == aliquot and x.analyte_id == analyte]
                    if (len(al) < 1):
                        user_defined1 = sheet.cell(row=row_idx, column=col_idx).value
                        al2 = AliquotAnalyte(aliquot, analyte, "", "", user_defined1)
                        lst_aliquot_analytes.append(al2)
                    else:
                        al[0] = sheet.cell(row=row_idx, column=col_idx).value

            data = list()
            for aliquot_analyte in lst_aliquot_analytes:
                row = self.get_template_dict()
                row["Aliquot"] = aliquot_analyte.aliquot
                row["Analyte Identifier"] = aliquot_analyte.analyte_id
                row["Analysis Date/Time"] = aliquot_analyte.analysis_datetime
                row["Measured Value"] = aliquot_analyte.measured_value
                row["User Defined 1"] = aliquot_analyte.user_defined1

                data.append(row)

            df = df.append(data, ignore_index=True)
            result.df = df
            result.status = "success"
            result.add_message("successfully processed file: {}".format(self.input_file))
            return result



        except Exception as e:
            result = Result()
            result.status = "failure"
            result.add_message(str(e))
            print(str(e))
            self.logger.error("Error processing file: {}  Error message: {}".format(self.input_file), str(e))
            return result