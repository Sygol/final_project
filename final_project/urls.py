"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import RegistrationView
from money_tracker.views import IndexView, CategoryFormView, UserCategoriesView, BalanceView, AddExpenseView, \
    AddIncomeView, DeleteTransactionView, UpdateExpenseView, UpdateIncomeView, check_balance, TransactionsView, \
    check_transactions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('newcategory', CategoryFormView.as_view(), name='new_category'),
    path('categories', UserCategoriesView.as_view(), name='categories'),
    path('balance', BalanceView.as_view(), name='balance'),
    path('newexpense', AddExpenseView.as_view(), name='add_expense'),
    path('newincome', AddIncomeView.as_view(), name='add_income'),
    path('delete/<int:pk>', DeleteTransactionView.as_view(), name='delete_transaction'),
    path('update/expense/<int:pk>', UpdateExpenseView.as_view(), name='update_expense'),
    path('update/income/<int:pk>', UpdateIncomeView.as_view(), name='update_income'),
    path('check_balance', check_balance, name='check_balance'),
    path('transactions', TransactionsView.as_view(), name='transactions'),
    path('check_transactions', check_transactions, name='check_transactions'),
]
