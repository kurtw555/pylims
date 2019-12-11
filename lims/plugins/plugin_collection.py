import inspect
import os
import pkgutil
import pandas as pd
import openpyxl


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
        self.pd = pd
        self.openpyxl = openpyxl

    def execute(self, processor):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError

    def check_input_file(self):
        ret_stat = ReturnStatus()
        if self.db_processor is None:            
            ret_stat.payload["status"] = "error"
            ret_stat.payload["message"] = "Could not find an input file"
            return ret_stat

        input_file = self.db_processor.input_file
        if not os.path.exists(input_file):
            ret_stat.payload["status"] = "error"
            ret_stat.payload["message"] = "Could not find an input file: " + input_file
            return ret_stat
            
        ret_stat.payload["status"] = "success"
        ret_stat.status = True
        return ret_stat




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