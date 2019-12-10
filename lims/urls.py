from django.urls import path

from lims import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('users/', views.users, name='users'),
    path('tasks/', views.tasks, name='tasks'),
    path('workflows/', views.workflows, name='workflows')
]
