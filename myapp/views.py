from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

def index(request):
  return render(request, 'index.html')

def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']

    user = auth.authenticate(username=email, password=password)

    if user is not None:
      auth.login(request, user)
      return redirect('/')
    else:
      messages.info(request, 'Credentials Invalid')
      return redirect ('login')
  else:
    return render(request, 'login.html')

def logout(request):
  auth.logout(request)
  return redirect('/')

def register(request):
  if request.method == 'POST':
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    confirmPassword = request.POST['confirmPassword']
    sex = request.POST['sex']
    color = request.POST['color']
    age = request.POST['age']

    if password == confirmPassword:
      if User.objects.filter(email=email).exists():
        messages.info(request, 'Email Already Used')
        return redirect('register')
      else:
        user = User.objects.create_user(
          name=name,
          username=email,
          email=email,
          password=password,
          sex=sex,
          color=color,
          age=age
        )
        user.save()

        return redirect('login')
    else:
      messages.info(request, 'Passwords do not match')
      return redirect('register')
  else:
    return render (request, 'register.html')

def tasks(request):
  return render (request, 'tasks.html')

def friends(request):
  return render (request, 'friends.html')

def invitations(request):
  return render (request, 'invitations.html')