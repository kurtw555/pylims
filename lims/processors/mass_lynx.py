from datetime import datetime
from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin
from ..result import Result

#from plugins.plugin_collection import PluginCollection
#from plugins.plugin_collection import Plugin


class MassLynx(Plugin):
    """This is the Mass Lynx data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'mass_lynx'
        self.description = 'Mass Lynx'
        self.version = '1.0'
        self.file_type = ".txt"

    def execute(self, file):

        try:

            aliquot = ""
            analysis_date_time = ""

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

            with open(self.input_file, mode="r") as file:
                idx_row = 0

                for line in file:
                    idx_row += 1
                    print(line)

                    if (idx_row < 20):
                        continue

                    line = line.strip()
                    #Should not be any more blank lines until we get to the end of the data
                    if len(line) < 1:
                        break

                    #The sheet can contain mulitple data sets
                    #The first row of each data set block contains the LIMS ID and analysis date
                    #e.g. SW846_01DEC_18-2,AW325-S-38-01,,,,,,01-Dec-18,13:34:02
                    #                      ^^^^^^^^^^^^^      ^^^^^^^^^^^^^^^^^^
                    #                       LIMS ID           analysis date time
                    #The data looks like:
                    #e.g. 1,PFOA,30,7.0112,0,214.703,4589,16.0753,dd,2.6196,0,412.9 > 369,,20,26712.1,607300,7.0112,,,,,0,7.0112,0,0,0,6.9624,7.0491,214.703,0,412.9 > 169,1,4.5385,1,47.307,1035,3.169,556.637,108.689,1e-012,1e-012,0,,
                    #       ^^^^             ^^^^^^^                 ^^^^^^
                    #     analyte id         Area                    Measured conc 

                    tokens = line.split(",")                    
                    #If this is an int then its data, otherwise start of new dataset
                    col1 = tokens[0]
                    if not col1.isnumeric():
                        aliquot = tokens[1]
                        date = tokens[len(tokens) - 2] + " " + tokens[len(tokens) -1]
                        analysis_date_time = datetime.strptime(date, "%d-%b-%y %H:%M:%S")
                        continue

                    analyte_id = tokens[1]

                    user_defined_1 = tokens[5]
                    if user_defined_1.strip() == "":
                        user_defined_1 = 0.0

                    measured_value = tokens[9]

                    row = self.get_template_dict()

                    row["Aliquot"] = aliquot
                    row["Analyte Identifier"] = analyte_id
                    row["Measured Value"] = measured_value
                    row["Analysis Date/Time"] = date
                    row["User Defined 1"] =user_defined_1

                    df = df.append(row, ignore_index=True)                    


        except Exception as e:
            result.status = "failure"
            result.add_message(str(e))
            print(str(e))
            self.logger.error("Error processing file: {}  Error message: {}".format(self.input_file), str(e))
            return result


        result.status = "success"
        result.df = df
        
        return result


        