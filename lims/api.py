
from django.core import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

import json

from lims.models import Task, Workflow, Processor


@csrf_exempt
@api_view(["POST"])
def login(request):
    """
    API endpoint that allows login.
    """
    print("request---")
    print(request)
    print("----------")

    try:
        data = json.loads(request.body)
        print("data: " + data["username"])
        return Response('Hello ' + data["username"] + ', welcome to the machine!')
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


def register(request):
    """
    API endpoint that allows new user registration.
    """


def logout(request):
    """
    API endpoint that allows logout.
    """


def users(request):
    """
    API endpoint that returns all tasks.
    """
    result = User.objects.all()
    resultJson = serializers.serialize('json', result)
    # TODO: send only required data
    return HttpResponse(resultJson, content_type='application/json')


def tasks(request):
    """
    API endpoint that returns all tasks.
    """
    result = Task.objects.all()
    resultJson = serializers.serialize('json', result)
    return HttpResponse(resultJson, content_type='application/json')


def workflows(request):
    """
    API endpoint that returns all workflows
    """
    result = Workflow.objects.all()
    resultJson = serializers.serialize('json', result)
    return HttpResponse(resultJson, content_type='application/json')


def processors(request):
    """
    API endpoint that returns all processors
    """
    result = Processor.objects.all()
    resultJson = serializers.serialize('json', result)
    print(resultJson)
    return HttpResponse(resultJson, content_type='application/json')
