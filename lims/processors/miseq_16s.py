from datetime import datetime
from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin
from ..result import Result


class MiSeq_16S(Plugin):
    """This is the MiSeq-16S data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'miseq_16s'
        self.description = 'Processor for MiSeq-16S data files'
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

            #Build list of aliquots
            lst_aliquots = list()
            for row_idx in range(2, num_rows + 1):                
                aliquot = sheet.cell(row=row_idx, column=1).value
                if aliquot == None or aliquot.strip() == "" or aliquot == "OTU":
                    break
                aliquot = aliquot.strip()                
                lst_aliquots.append(aliquot)


            row_kingdom = 0
            row_phylum = 0
            row_class = 0
            row_order = 0
            row_family = 0
            row_genus = 0
            #Get description row range            
            for row_idx in range(len(lst_aliquots) +2, num_rows + 1):
                cell_val = sheet.cell(row=row_idx, column=1).value
                if cell_val is None:
                    continue
                cell_val = cell_val.strip().lower()
                if cell_val == "kingdom": row_kingdom = row_idx                    
                elif cell_val == "phylum": row_phylum = row_idx
                elif cell_val == "class":  row_class = row_idx
                elif cell_val == "order":  row_order = row_idx
                elif cell_val == "family": row_family = row_idx
                elif cell_val == "genus":  row_genus = row_idx                
            

            #Build list of analyte ids
            lst_analytes = list()
            for col_idx in range(2, num_cols + 1):
                analyte = sheet.cell(row=1, column=col_idx).value
                if analyte is None:
                    break
                analyte = analyte.strip()
                if analyte == "":
                    break
                lst_analytes.append(analyte)

            #Loop over data to get measured values
            data = list()
            for row_idx in range(2, len(lst_aliquots) +1):
                
                for col_idx in range(2, len(lst_analytes) + 1):
                    row = self.get_template_dict()

                    row["Aliquot"] = lst_aliquots[row_idx - 2]
                    row["Analyte Identifier"] = lst_analytes[col_idx - 2]
                    measured_val = sheet.cell(row=row_idx, column=col_idx).value
                    #If meausured value is None set to 0              
                    if measured_val is not None:                        
                        if not self.is_number(measured_val):
                            measured_val = 0
                    else:
                        measured_val = 0

                    row["Measured Value"] = measured_val

                    desc = sheet.cell(row=row_kingdom, column=col_idx).value + ";"
                    desc += sheet.cell(row=row_phylum, column=col_idx).value + ";"
                    desc += sheet.cell(row=row_class, column=col_idx).value + ";"
                    desc += sheet.cell(row=row_order, column=col_idx).value + ";"
                    desc += sheet.cell(row=row_family, column=col_idx).value + ";"
                    desc += sheet.cell(row=row_genus, column=col_idx).value
                    row["Description"] = desc

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