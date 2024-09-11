from django.contrib import admin
from .models import ToDoTask, Priority, Invite

# Register your models here.
admin.site.register(ToDoTask)
admin.site.register(Priority)
admin.site.register(Invite)