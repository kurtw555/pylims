from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin

#from plugins.plugin_collection import PluginCollection
#from plugins.plugin_collection import Plugin


class Qubit2_0(Plugin):
    """This is the Qubit2.0 data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'qubit2_0'
        self.description = 'Processor for Qubit 2.0 data files'

    def execute(self, processor):
        df = self.pd.read_csv("TestBookFull.csv")        
        return df