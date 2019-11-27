from itertools import chain

from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView

from money_tracker.forms import UserCategoryForm, UserExpensesForm
from money_tracker.models import Category, Transaction
from money_tracker.scripts import range_of_current_month


class IndexView(TemplateView):
    template_name = 'money_tracker/index.html'


class CategoryFormView(CreateView):
    template_name = 'money_tracker/add_category.html'
    form_class = UserCategoryForm
    success_url = reverse_lazy('index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class UserCategoriesView(ListView):
    template_name = 'money_tracker/list_categories.html'

    def get_queryset(self):
        return Category.objects.filter(Q(user=self.request.user, expense_or_income_choices='EXPENSE') | Q(user=None,
                                       expense_or_income_choices='EXPENSE'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['income_list'] = Category.objects.filter(Q(user=self.request.user, expense_or_income_choices='INCOME') |
                                                         Q(user=None, expense_or_income_choices='INCOME'))
        return context


class BalanceView(TemplateView):
    template_name = 'money_tracker/balance.html'

    def get_context_data(self, *args, **kwargs):
        month, year, month_start, month_end = range_of_current_month()
        context = super().get_context_data(*args, **kwargs)
        income = sum(Transaction.objects.filter(user=self.request.user, category__expense_or_income_choices='INCOME',
                                                date__lte=month_end, date__gte=month_start).values_list('amount', flat=True)) \
               + sum(Transaction.objects.filter(user=self.request.user, user_category__expense_or_income_choices='INCOME',
                                                date__lte=month_end, date__gte=month_start).values_list('amount', flat=True))
        expense = sum(Transaction.objects.filter(user=self.request.user, category__expense_or_income_choices='EXPENSE',
                                                date__lte=month_end, date__gte=month_start).values_list('amount', flat=True)) \
                + sum(Transaction.objects.filter(user=self.request.user, user_category__expense_or_income_choices='EXPENSE',
                                                date__lte=month_end, date__gte=month_start).values_list('amount', flat=True))
        income_transactions = Transaction.objects.filter(Q(user=self.request.user, category__expense_or_income_choices='INCOME',
                                                         date__lte=month_end, date__gte=month_start) | Q(user=self.request.user,
                                                         user_category__expense_or_income_choices='INCOME', date__lte=month_end,
                                                         date__gte=month_start))
        expense_transactions = Transaction.objects.filter(Q(user=self.request.user, category__expense_or_income_choices='EXPENSE',
                                                         date__lte=month_end, date__gte=month_start) | Q(user=self.request.user,
                                                         user_category__expense_or_income_choices='EXPENSE', date__lte=month_end,
                                                         date__gte=month_start))
        context['income'] = income
        context['expense'] = expense
        context['balance'] = income - expense
        context['month'] = month
        context['year'] = year
        context['income_transaction'] = income_transactions
        context['expense_transaction'] = expense_transactions
        return context


class AddExpenseView(CreateView):
    template_name = 'money_tracker/add_expense.html'
    form_class = UserExpensesForm
    success_url = reverse_lazy('balance')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
