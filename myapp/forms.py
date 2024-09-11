from django import forms
from .models import ToDoTask, Priority

class RegisterForm(forms.Form):
  name = forms.CharField(min_length=2, max_length=150, error_messages={'required': 'Name is required.'})
  email = forms.EmailField(error_messages={'required': 'Email is required.'})
  password = forms.CharField(
    widget=forms.PasswordInput(), 
    min_length=3, 
    error_messages={'required': 'Password is required.', 'min_length': 'Password must be at least 3 characters long.'}
    )
  confirm_password = forms.CharField(
    widget=forms.PasswordInput(), 
    error_messages={'required': 'Please confirm your password.'}
    )
  sex = forms.ChoiceField(choices=[
    ('', 'Sex'), 
    ('male', 'Male'), 
    ('female', 'Female'), 
    ('dontAnswer', "Don't Answer")
    ], error_messages={'required': 'Please select your gender.'})
  color = forms.ChoiceField(choices=[
    ('', 'Color'), 
    ('blue', 'Blue'), 
    ('pink', 'Pink'), 
    ('green', 'Green')
    ], error_messages={'required': 'Please select a color.'})
  age = forms.ChoiceField(choices=[
    ('', 'Age'), 
    ('18orLess', '18 or Less'), 
    ('19to25', '19 to 25'), 
    ('26to35', '26 to 35'), 
    ('36to45', '36 to 45'), 
    ('45orAbove', '45 or Above')
    ], error_messages={'required': 'Please select your age.'})
  
  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')

    if password and confirm_password and password != confirm_password:
      self.add_error('confirm_password', 'Passwords do not match.')
      
      
class LoginForm(forms.Form):
  email = forms.EmailField(error_messages={'required': 'Email is required.'})
  password = forms.CharField(
    widget=forms.PasswordInput(), 
    min_length=3, 
    error_messages={'required': 'Password is required.', 'min_length': 'Password must be at least 3 characters long.'}
    )
  
class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = ToDoTask
        fields = ['title', 'description', 'priority']

    title = forms.CharField(
        min_length=3, 
        max_length=80,
        error_messages={'required': 'You need to add a title', 'min_length': 'Your title is too short', 'max_length': 'Your title must not exceed 80 letters'},
        widget=forms.TextInput(attrs={
          'class': 'form-control', 
          'placeholder': 'Title',
          'id': 'title'
        })
    )
    description = forms.CharField(
        min_length=5, 
        max_length=400,
        error_messages={'required': 'You need to add a description', 'min_length': 'Your description is too short', 'max_length': 'Your description must not exceed 400 letters'},
        widget=forms.Textarea(attrs={
          'class': 'form-control', 
          'placeholder': 'Description',
          'id': 'TaskDescription', 
          'style': 'height: 120px'
        })
    )
    priority = forms.ModelChoiceField(
        queryset=Priority.objects.all(),
        empty_label="Select a priority",
        error_messages={'required': 'Please select a priority level.'},
        widget=forms.Select(attrs={
          'class': 'form-select', 
          'id': 'priority'
        })
    )
    
    