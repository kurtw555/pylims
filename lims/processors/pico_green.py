from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin

#from plugins.plugin_collection import PluginCollection
#from plugins.plugin_collection import Plugin


class PicoGreen(Plugin):
    """This is the Pico Green data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'pico_green'
        self.description = 'Processor for PicoGreen data files'

    def execute(self, processor):        
        df = self.pd.read_csv("TestBookFull.csv")        
        return df