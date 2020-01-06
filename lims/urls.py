from django.urls import path

from lims import api

urlpatterns = [
    path('users/', api.users, name='users'),
    path('tasks/', api.tasks, name='tasks'),
    path('workflows/', api.workflows, name='workflows'),
    path('processors/', api.processors, name='processors')
]
