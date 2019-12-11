from django.urls import path

from lims import api

urlpatterns = [
    path('register', api.register, name='register'),
    path('login', api.login, name='login'),
    path('logout', api.logout, name='logout'),
    path('users/', api.users, name='users'),
    path('tasks/', api.tasks, name='tasks'),
    path('workflows/', api.workflows, name='workflows')
]
