
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse

from lims.models import Task, Workflow, Processor


def register(request):
    """
    API endpoint that allows new user registration.
    """
    print(request.POST['username'] + ' | ' + request.POST['password'])


def login(request):
    """
    API endpoint that allows login.
    """
    print(request.POST['username'] + ' | ' + request.POST['password'])


def logout(request):
    """
    API endpoint that allows logout.
    """


def users(request):
    """
    API endpoint that returns all tasks.
    """
    return HttpResponse(User.objects.all())


def tasks(request):
    print('inside the tasks handler!')
    """
    API endpoint that returns all tasks.
    """
    return HttpResponse(DBTask.objects.all())


def workflows(request):
    """
    API endpoint that returns all workflows
    """
    return HttpResponse(DBWorkflow.objects.all())
