from itertools import chain

from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView

from money_tracker.forms import UserCategoryForm
from money_tracker.models import Category, UserCategory, Transaction
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
        expense_categories = Category.objects.filter(expense_or_income_choices='EXPENSE')
        expense_user_categories = UserCategory.objects.filter(user=self.request.user, expense_or_income_choices='EXPENSE')
        result = list(chain(expense_categories, expense_user_categories))
        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        income_categories = Category.objects.filter(expense_or_income_choices='INCOME')
        income_user_categories = UserCategory.objects.filter(user=self.request.user, expense_or_income_choices='INCOME')
        result = list(chain(income_categories, income_user_categories))
        context['income_list'] = result
        return context


class BalanceView(TemplateView):
    template_name = 'money_tracker/balance.html'

    def get_context_data(self, *args, **kwargs):
        month, month_start, month_end = range_of_current_month()
        context = super().get_context_data(*args, **kwargs)
        income = sum(Transaction.objects.filter(user=self.request.user, category__expense_or_income_choices='INCOME',
                                                date__lte=month_end, date__gte=month_start).values_list('amount', flat=True)) \
               + sum(Transaction.objects.filter(user=self.request.user, user_category__expense_or_income_choices='INCOME',
                                                date__lte=month_end, date__gte=month_start).values_list('amount', flat=True))
        expense = sum(Transaction.objects.filter(user=self.request.user, category__expense_or_income_choices='EXPENSE',
                                                date__lte=month_end, date__gte=month_start).values_list('amount', flat=True)) \
                + sum(Transaction.objects.filter(user=self.request.user, user_category__expense_or_income_choices='EXPENSE',
                                                date__lte=month_end, date__gte=month_start).values_list('amount', flat=True))
        context['income'] = income
        context['expense'] = expense
        context['balance'] = income - expense
        context['month'] = month
        return context
