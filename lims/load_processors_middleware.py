from django.core.exceptions import MiddlewareNotUsed
from .models import Processor, Task
from lims.serializers import ProcessorSerializer
from lims.plugins.plugin_collection import PluginCollection

#Used to initialize the processors in the database on startup
class LoadProcessorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        pc = PluginCollection("lims.processors")
        plug_processors = pc.plugins

        dct_procs = dict()
        processors = Processor.objects.all()
        for proc in processors:
            proc2 = proc
            proc.enabled = False
            proc.save()
            dct_procs[proc.name.lower()] = proc

        lst_db_processors = list()
        for proc in plug_processors:
            if proc.name.lower() in dct_procs:
                dct_procs[proc.name.lower()].enabled = True
                dct_procs[proc.name.lower()].save()
            else:
                new_proc = Processor(name=proc.name, version=proc.version, description=proc.description, file_type=proc.file_type, enabled=True)
                lst_db_processors.append(new_proc)
                
        if len(lst_db_processors) > 0:
            Processor.objects.bulk_create(lst_db_processors)
        #serializer = ProcessorSerializer(processors, many=True)

        raise MiddlewareNotUsed
