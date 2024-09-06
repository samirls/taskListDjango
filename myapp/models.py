from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    name = models.CharField(max_length=150, verbose_name=_("Name"), help_text=_("Write your Name"))
    sex = models.CharField(max_length=10, verbose_name=_("Sex"), help_text=_("Inform your sex"))
    color = models.CharField(max_length=30, verbose_name=_("Favorite Color"), help_text=_("Inform a color"))
    age = models.CharField(
        max_length=30,
        verbose_name=_("Age"), 
        help_text=_("Inform your age")
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text=_("The groups this user belongs to."),
        verbose_name=_("groups"),
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text=_("Specific permissions for this user."),
        verbose_name=_("user permissions"),
    )
    
    def __str__(self):
        return self.username

class Priority(models.Model):
    level = models.CharField(max_length=50, verbose_name=_("Priority Level"), help_text=_("Inform the priority level"))

    def __str__(self):
        return self.level

class ToDoTask(models.Model):
    title = models.CharField(max_length=80, verbose_name=_("Title"), help_text=_("You need to add a title"))
    description = models.CharField(max_length=400, verbose_name=_("Description"), help_text=_("You need to add a description"))
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    lastUpdate = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated At"))
    
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, related_name="tasks", verbose_name=_("Priority"))
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks", verbose_name=_("User"))

    def __str__(self):
        return self.title



  
