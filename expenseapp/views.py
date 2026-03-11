from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import SignupForm
from django.views import View
from .models import Expense
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ExpenseForm
from django.db.models import Q

#===============================================================

class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form':form})
    
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('expense_list')
        return render(request, 'signup.html', {'form':form})
    
class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('expense_list')
        return render(request, 'login.html', {'form':form})
    
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')
#==============================================================
     
class ExpenseList(LoginRequiredMixin, View):

    def get(self, request):

        expenses = Expense.objects.filter(user=request.user).order_by('-date')
        #filter category expenselist
        category = request.GET.get('category')
        if category and category != "All":
            expenses = expenses.filter(category=category)
        #search field
        search = request.GET.get('search')
        if search:
            expenses = expenses.filter(
                Q(category__icontains=search) | 
                Q(amount__icontains=search)
                )
        return render(request, 'expense_list.html', {'expenses': expenses, 'category':category})
    
class AddExpense(LoginRequiredMixin, View):

    def get(self, request):
        form = ExpenseForm()
        return render(request, 'add_expense.html', {'form': form})

    def post(self, request):
        form = ExpenseForm(request.POST)
# giggkj
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')

        return render(request, 'add_expense.html', {'form': form})
    
#===========================================================

class UpdateExpense(View):
    def get(self, request, id):
        expense = Expense.objects.get(id=id, user = request.user)
        form = ExpenseForm(instance=expense)
        return render(request, 'updateexpense.html', {'form':form})
    
    def post(self, request, id):
        expense = Expense.objects.get(id=id, user= request.user)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
        return render(request, 'updateexpense.html', {'form':form})
    
class DeleteExpense(LoginRequiredMixin, View):

    def post(self, request, pk):
        expense = Expense.objects.get(pk=pk, user=request.user)
        expense.delete()
        return redirect('expense_list')