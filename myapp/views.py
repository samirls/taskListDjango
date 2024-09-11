from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import RegisterForm, LoginForm, CreateTaskForm
from django.contrib.auth.decorators import login_required
from .models import Priority, ToDoTask, CustomUser, Invite, Friendship, UserToDoTask
from django.db.models import Q

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
    user_tasks = UserToDoTask.objects.filter(user=request.user)
    
    context = {
        'user_tasks': user_tasks
    }
    return render(request, 'tasks.html', context)

def createNewTask(request):
  if request.method == 'POST':
    form = CreateTaskForm(request.POST)
    if form.is_valid():
      task = form.save(commit=False)
      task.user = request.user
      task.save()
      
      user_to_do_task = UserToDoTask(
        user=request.user,
        task=task
      )
      user_to_do_task.save()
      messages.success(request, 'Task created successfully')
      return redirect('tasks')
    else:
      messages.error(request, 'Please correct the errors and try again.')
      priorities = Priority.objects.all()
      context = {
        'form': form,
        'priorities': priorities
        }
      return render(request, 'createNewTask.html', context)
  else:
    form = CreateTaskForm()
    priorities = Priority.objects.all()
    context = {
      'form': form,
      'priorities': priorities
    }
    return render (request, 'createNewTask.html', context)

@login_required
def editTask(request, task_id):
    task = get_object_or_404(ToDoTask, id=task_id, user=request.user)

    if request.method == 'POST':
        form = CreateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('tasks')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CreateTaskForm(instance=task)

    context = {
        'form': form,
        'task': task
    }
    return render(request, 'editTask.html', context)
  
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(ToDoTask, id=task_id, user=request.user)

    if request.method == "POST":
        task.delete()
        return JsonResponse({'success': True}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def friends(request):
  user = request.user
  
  friendships = Friendship.objects.filter(
    Q(user=user) | Q(friend=user)
  ).select_related('user', 'friend')
  
  friend_list = [
    f.friend if f.user == user else f.user
    for f in friendships
  ]

  context = {
    'friends': friend_list
  }
  
  return render(request, 'friends.html', context)

@login_required
def add_friend(request):
  if request.method == 'POST':
    friend_email = request.POST.get('FriendEmail')
    user = request.user
    try:
      friend = CustomUser.objects.get(email=friend_email)
    except CustomUser.DoesNotExist:
      messages.error(request, 'Friend not found.')
      return redirect('friends')
        
    if friend_email == user.email:
      messages.error(request, 'You cannot add yourself.')
      return redirect('friends')
        
    is_friend_already_invited = Invite.objects.filter(sender=user, receiver=friend).exists()
    if is_friend_already_invited:
      messages.error(request, 'Friend already invited.')
      return redirect('friends')
          
    am_i_already_invited_by_friend = Invite.objects.filter(sender=friend, receiver=user).exists()
    if am_i_already_invited_by_friend:
      messages.error(request, 'This friend already invited you. Manage your friends.')
      return redirect('friends')
          
    invite = Invite(sender=user, receiver=friend, invite_status=Invite.InviteStatus.PENDING)
    invite.save()
        
    messages.success(request, 'Invite sent!')
    return redirect('friends')
  else:
      return redirect('friends')

@login_required
def invitations(request):
    user = request.user

    sent_invites = Invite.objects.filter(sender=user)
    received_invites = Invite.objects.filter(receiver=user)

    return render(request, 'invitations.html', {
        'sent_invites': sent_invites,
        'received_invites': received_invites
    })
    
@login_required
def change_invite_status(request, invite_id, action):
    invite = get_object_or_404(Invite, id=invite_id)

    if action == 'mark-as-read':
      invite.invite_status = Invite.InviteStatus.READ
      messages.success(request, 'Invite marked as read')
      invite.save()
      return redirect('invitations')
    
    elif action == 'mark-as-unread':
      invite.invite_status = Invite.InviteStatus.PENDING
      messages.success(request, 'Invite marked as Unread')
      invite.save()
      return redirect('invitations')
    
    elif action == 'accept':
      invite.invite_status = Invite.InviteStatus.ACCEPTED
      Friendship.objects.create(
        user=invite.sender,
        friend=invite.receiver
      )
      messages.success(request, 'Friend added successfully')
      invite.save()
      return redirect('invitations')
    
    elif action == 'delete':
      invite.delete()
      Friendship.objects.filter(
        Q(user=invite.sender, friend=invite.receiver) |
        Q(user=invite.receiver, friend=invite.sender)
        ).delete()

      messages.success(request, 'Invite and friendship deleted successfully')
      return redirect('invitations')
    else:
        return redirect('invitations')