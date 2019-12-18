from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin

#from plugins.plugin_collection import PluginCollection
#from plugins.plugin_collection import Plugin


class Tracefinder(Plugin):
    """This is the Tracefinder data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'tracefinder'
        self.description = 'Processor for Tracefinder data files'

    def execute(self, processor):
        df = self.pd.read_csv("TestBookFull.csv")        
        return df