from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter Your Search : ")
    
class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']
        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
             forms.CheckboxInput(attrs={'class': 'form-check-input'}): 'is_finished'
        }
        
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
