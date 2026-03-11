from django.urls import path
from .views import *

urlpatterns = [
    #page urls
    path('', ExpenseList.as_view(), name='expense_list'),
    path('add-expense/', AddExpense.as_view(), name='add_expense'),
    path('update-expense/<int:id>/', UpdateExpense.as_view(), name='update_expense'),
    path('delete-expense/<int:pk>/', DeleteExpense.as_view(), name='delete_expense'),
    #authentication urls
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]