from django.apps import AppConfig
from lims.models import Task, Workflow, Processor
from lims.plugins.plugin_collection import PluginCollection


class LimsConfig(AppConfig):
    name = 'lims'
