
from django.core import serializers
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

import json

from lims.models import Task, Workflow, Processor
from lims.plugins.plugin_collection import PluginCollection
from lims.serializers import WorkflowSerializer, TaskSerializer


@api_view(['GET'])
def users(request):
    """
    API endpoint that returns all users.
    """
    result = User.objects.all()
    resultJson = serializers.serialize('json', result)
    # TODO: send only required data
    return HttpResponse(resultJson, content_type='application/json')


@api_view(['GET', 'POST'])
def tasks(request):
    """
    API endpoint that returns all tasks or creates a task
    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
        #resultJson = serializers.serialize('json', result)
        # return HttpResponse(resultJson, content_type='application/json')
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def workflows(request):
    """
    API endpoint that returns all workflows or creates new workflow
    """
    if request.method == 'GET':
        workflows = Workflow.objects.all()
        serializer = WorkflowSerializer(workflows, many=True)
        return Response(serializer.data)
        #resultJson = serializers.serialize('json', result)
        # return HttpResponse(resultJson, content_type='application/json')
    elif request.method == 'POST':
        serializer = WorkflowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def processors(request):
    """
    API endpoint that returns all processors
    """
    if request.method == 'GET':
        pc = PluginCollection("lims.processors")
        plug_processors = pc.plugins

        result = Processor.objects.all()
        resultJson = serializers.serialize('json', result)
        return HttpResponse(resultJson, content_type='application/json')
    elif request.method == 'POST':
        return Response({'message': 'POST to this endpoint is not yet enabled'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
