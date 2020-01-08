import inspect
import os
import pathlib
import logging
import pkgutil
import pandas as pd
import openpyxl
from ..result import Result


class Plugin():
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    def __init__(self):
        self.id = 'UNKNOWN'
        self.name = 'UNKNOWN'
        self.description = 'UNKNOWN'
        self.file_type = 'UNKNOWN'
        self.input_file = 'UNKNOWN'
        self.logger = logging.getLogger("LIMS_Run_Processor")
        self.pd = pd
        self.openpyxl = openpyxl

    def execute(self, file):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError

    def input_file_exists(self):
        #ret_stat = ReturnStatus()        
        
        file = pathlib.Path(self.input_file)
        if file.exists():
            return True
        else:
            return False
        #if not os.path.exists(self.input_file):
        #   return False

    def get_base_file_name(self):
        base = os.path.basename(self.input_file)
        file_no_ext = os.path.splitext(base)[0]
        return file_no_ext

     #Check if a string value is a number
    def is_number(self, str_val):
        try:
            val = int(str_val)
            return True

        except ValueError:
            try:
                val = float(str_val)
                return True
            except ValueError:
                return False

        return False

    def get_template_dict(self):
        data = {'Aliquot':'',
            	'Analyte Identifier':'',
                'Measured Value':'',
                'Units':'',
                'Dilution Factor':'',
                'Analysis Date/Time':'',
                'Comment':'',
                'Description':'',
                'User Defined 1':'',
                'User Defined 2':'',
                'User Defined 3':'',
                'User Defined 4':'',
                'User Defined 5':'',
                'User Defined 6':'',
                'User Defined 7':'',
                'User Defined 8':'',
                'User Defined 9':'',
                'User Defined 10':'',
                'User Defined 11':'',
                'User Defined 12':'',
                'User Defined 13':'',
                'User Defined 14':'',
                'User Defined 15':'',
                'User Defined 16':'',
                'User Defined 17':'',
                'User Defined 18':'',
                'User Defined 19':'',
                'User Defined 20':''
        }
        return data


    def get_empty_dataframe(self):
        data = self.get_template_dict()
        df = pd.DataFrame(data, index=[0])
        df = df.drop(df.index[0])
        return df




class PluginCollection():
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    def __init__(self, plugin_package):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_package = plugin_package
        self.reload_plugins()
        

    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """        
        self.plugins = []
        self.seen_paths = []
        print()
        print(f'Looking for plugins under package {self.plugin_package}')
        self.walk_package(self.plugin_package)

    
    def execute(self, processor):
        if self.plugins is None:
            return None
            
        for plugin in self.plugins:
            if plugin.name.lower().strip() == processor.strip():
                return plugin.execute(processor)





    def apply_all_plugins_on_value(self, argument):
        """Apply all of the plugins on the argument supplied to this function
        """
        print()
        print(f'Applying all plugins on value {argument}:')
        for plugin in self.plugins:
            print(f'    Applying {plugin.description} on value {argument} yields value {plugin.execute(argument)}')

    def walk_package(self, package):
        """Recursively walk the supplied package to retrieve all plugins
        """
        imported_package = __import__(package, fromlist=['blah'])

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                plugin_module = __import__(pluginname, fromlist=['blah'])
                clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    if issubclass(c, Plugin) & (c is not Plugin):
                        print(f'    Found plugin class: {c.__module__}.{c.__name__}')
                        self.plugins.append(c())


        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # Get all sub directory of the current package path directory
                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

                # For each sub directory, apply the walk_package method recursively
                for child_pkg in child_pkgs:
                    self.walk_package(package + '.' + child_pkg)