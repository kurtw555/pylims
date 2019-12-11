from lims.plugins.plugin_collection import PluginCollection
from lims.plugins.plugin_collection import Plugin

#from plugins.plugin_collection import PluginCollection
#from plugins.plugin_collection import Plugin


class MassLynx(Plugin):
    """This is the Mass Lynx data processor"""

    def __init__(self):
        super().__init__()
        self.name = 'mass_lynx'
        self.description = 'Mass Lynx'
        self.file_type = ".txt"

    def execute(self, processor):
        data = self.pd.read_csv("TestBookFull.csv")
        return processor * -1