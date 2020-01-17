from django.core import serializers
from django.contrib.auth.models import User

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

import lims.utilities as utils
from lims.models import Task, Workflow, Processor
from lims.plugins.plugin_collection import PluginCollection
from lims.processing import GenerateTask
from lims.serializers import UserSerializer, WorkflowSerializer, ProcessorSerializer, TaskSerializer


@api_view(['GET'])
def users(request):
    """
    API endpoint that returns all users.
    """
    permission_classes = [IsAuthenticated]
    
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def tasks(request):
    """
    API endpoint that returns all tasks or creates a task
    """
    permission_classes = [IsAuthenticated]

    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'PATCH'])
def workflows(request):
    """
    API endpoint that returns all workflows or creates new workflow
    """
    permission_classes = [IsAuthenticated]
    if request.method == 'GET':
        workflows = Workflow.objects.all()
        serializer = WorkflowSerializer(workflows, many=True)
        return Response(serializer.data)
    else:
        serializer = WorkflowSerializer(data=request.data)
        if serializer.is_valid():
            workflow = serializer.save()
            paths = utils.generate_directories(workflow.name)
            workflow.v_input_path = paths[0]
            workflow.v_output_path = paths[1]
            workflow.save()
            utils.update_file_config(workflow.id, workflow.name, workflow.input_path, workflow.output_path, workflow.v_input_path, workflow.v_output_path)
            GenerateTask(workflow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def processors(request):
    """
    API endpoint that returns all processors
    """
    permission_classes = [IsAuthenticated]

    if request.method == 'GET':
        pc = PluginCollection("lims.processors")
        plug_processors = pc.plugins

        processors = Processor.objects.all()
        serializer = ProcessorSerializer(processors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        return Response({'message': 'POST to this endpoint is not yet enabled'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
