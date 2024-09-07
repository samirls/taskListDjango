from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required

User = get_user_model()

def index(request):
  return render(request, 'index.html')

def login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = auth.authenticate(username=email, password=password)
      if user is not None:
        auth.login(request, user)
        messages.success(request, 'You are logged in!')
        return redirect('tasks')
      else:
        messages.error(request, 'Invalid credentials')
    else:
      messages.error(request, 'Invalid form submission')
  else:
    if 'next' in request.GET:
      messages.error(request, 'Log in first')
      
  return render(request, 'login.html')

def logout(request):
  auth.logout(request)
  return redirect('/')

def register(request):
  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      name = form.cleaned_data['name']
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      sex = form.cleaned_data['sex']
      color = form.cleaned_data['color']
      age = form.cleaned_data['age']

      if User.objects.filter(email=email).exists():
        messages.error(request, 'Email Already Used')
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
      messages.error(request, 'Form submission failed. Please correct the errors and try again.')
  else:
    form = RegisterForm()
    
  return render(request, 'register.html', {'form': form})

@login_required
def tasks(request):
  return render (request, 'tasks.html')

def createNewTask(request):
  return render (request, 'createNewTask.html')

@login_required
def friends(request):
  return render (request, 'friends.html')

@login_required
def invitations(request):
  return render (request, 'invitations.html')