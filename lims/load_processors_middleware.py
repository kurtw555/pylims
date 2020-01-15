from django.core.exceptions import MiddlewareNotUsed
from .models import Processor
from lims.serializers import ProcessorSerializer
from lims.plugins.plugin_collection import PluginCollection

#Used to initialize the processors in the database on startup
class LoadProcessorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        pc = PluginCollection("lims.processors")
        plug_processors = pc.plugins

        processors = Processor.objects.all()
        for proc in processors:
            proc2 = proc
        serializer = ProcessorSerializer(processors, many=True)

        raise MiddlewareNotUsed

        
