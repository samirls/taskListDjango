from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  path('register', views.register, name='register'),
  path('tasks', views.tasks, name='tasks'),
  path('tasks/createNewTask', views.createNewTask, name='createNewTask'),
  path('tasks/edit/<int:task_id>/', views.editTask, name='editTask'),
  path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
  path('friends', views.friends, name='friends'),
  path('add_friend/', views.add_friend, name='add_friend'),
  path('invitations', views.invitations, name='invitations'),
  path('invitations/change-status/<int:invite_id>/<str:action>/', views.change_invite_status, name='change_invite_status'),
]