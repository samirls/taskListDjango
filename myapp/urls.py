from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  path('register', views.register, name='register'),
  path('tasks', views.tasks, name='tasks'),
  path('friends', views.friends, name='friends'),
  path('invitations', views.invitations, name='invitations'),
]