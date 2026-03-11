from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Expense
from django import forms

#===================================================

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'category', 'date']