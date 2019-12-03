import calendar
from itertools import chain

from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView

from money_tracker.forms import UserCategoryForm, UserExpensesForm, UserIncomeForm, UserTransactionForm
from money_tracker.models import Category, Transaction
from money_tracker.scripts import range_of_current_month, month_name_to_number


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
        income = sum(Transaction.objects.filter((Q(user=self.request.user) | Q(user=None)) &
                                                Q(category__expense_or_income_choices='INCOME', date__lte=month_end,
                                                  date__gte=month_start)).values_list('amount', flat=True))
        expense = sum(Transaction.objects.filter((Q(user=self.request.user) | Q(user=None)) &
                                                 Q(category__expense_or_income_choices='EXPENSE', date__lte=month_end,
                                                   date__gte=month_start)).values_list('amount', flat=True))
        income_transactions = Transaction.objects.values('category__name').annotate(sum_transactions=Sum('amount')).filter((Q(user=self.request.user) | Q(user=None)) &
                                                         Q(category__expense_or_income_choices='INCOME',
                                                         date__lte=month_end, date__gte=month_start)).order_by('-sum_transactions')
        expense_transactions = Transaction.objects.values('category__name').annotate(sum_transactions=Sum('amount')).filter((Q(user=self.request.user) | Q(user=None)) &
                                                         Q(category__expense_or_income_choices='EXPENSE',
                                                         date__lte=month_end, date__gte=month_start)).order_by('-sum_transactions')
        context['income'] = income
        context['expense'] = expense
        context['balance'] = income - expense
        context['month'] = month
        context['year'] = year
        context['income_transaction'] = [[income_trans['category__name'], round(income_trans['sum_transactions'], 2)] for income_trans in income_transactions]
        context['expense_transaction'] = [[expense_trans['category__name'], round(expense_trans['sum_transactions'], 2)] for expense_trans in expense_transactions]
        return context


class AddExpenseView(CreateView):
    template_name = 'money_tracker/add_expense.html'
    form_class = UserTransactionForm
    success_url = reverse_lazy('balance')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class AddIncomeView(CreateView):
    template_name = 'money_tracker/add_income.html'
    form_class = UserTransactionForm
    success_url = reverse_lazy('balance')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class DeleteTransactionView(DeleteView):
    model = Transaction
    success_url = reverse_lazy('balance')


class UpdateExpenseView(UpdateView):
    form_class = UserTransactionForm
    model = Transaction
    success_url = reverse_lazy('balance')
    template_name_suffix = '_expense_form'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_initial(self):
        item = Transaction.objects.get(pk=self.kwargs.get('pk'))
        initial = super().get_initial()
        initial['category'] = item.category
        return initial


class UpdateIncomeView(UpdateView):
    form_class = UserTransactionForm
    model = Transaction
    success_url = reverse_lazy('balance')
    template_name_suffix = '_income_form'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_initial(self):
        item = Transaction.objects.get(pk=self.kwargs.get('pk'))
        initial = super().get_initial()
        initial['category'] = item.category
        return initial


class TransactionsView(TemplateView):
    template_name = 'money_tracker/transactions.html'

    def get_context_data(self, *args, **kwargs):
        month, year, month_start, month_end = range_of_current_month()
        context = super().get_context_data(*args, **kwargs)
        income = sum(Transaction.objects.filter((Q(user=self.request.user) | Q(user=None)) &
                                                Q(category__expense_or_income_choices='INCOME', date__lte=month_end,
                                                  date__gte=month_start)).values_list('amount', flat=True))
        expense = sum(Transaction.objects.filter((Q(user=self.request.user) | Q(user=None)) &
                                                 Q(category__expense_or_income_choices='EXPENSE', date__lte=month_end,
                                                   date__gte=month_start)).values_list('amount', flat=True))
        income_transactions = Transaction.objects.filter((Q(user=self.request.user) | Q(user=None)) &
                                                Q(category__expense_or_income_choices='INCOME', date__lte=month_end,
                                                  date__gte=month_start)).order_by('-date')
        expense_transactions = Transaction.objects.filter((Q(user=self.request.user) | Q(user=None)) &
                                                Q(category__expense_or_income_choices='EXPENSE', date__lte=month_end,
                                                  date__gte=month_start)).order_by('-date')
        context['income'] = income
        context['expense'] = expense
        context['balance'] = income - expense
        context['month'] = month
        context['year'] = year
        context['income_transaction'] = income_transactions
        context['expense_transaction'] = expense_transactions
        return context


def check_balance(request):
    month = request.GET.get('month')
    year = int(request.GET.get('year'))
    month = int(month_name_to_number(month))
    month_range = calendar.monthrange(year, month)
    month_end = str(year)+'-'+str(month)+'-'+str(month_range[1])
    month_start = str(year)+'-'+str(month)+'-01'
    income = sum(Transaction.objects.filter((Q(user=request.user) | Q(user=None)) &
                                            Q(category__expense_or_income_choices='INCOME', date__lte=month_end,
                                              date__gte=month_start)).values_list('amount', flat=True))
    expense = sum(Transaction.objects.filter((Q(user=request.user) | Q(user=None)) &
                                             Q(category__expense_or_income_choices='EXPENSE', date__lte=month_end,
                                               date__gte=month_start)).values_list('amount', flat=True))
    income_groupby = list(Transaction.objects.values('category__name').annotate(sum_transactions=Sum('amount')).filter((Q(user=request.user) | Q(user=None)) &
                                                         Q(category__expense_or_income_choices='INCOME',
                                                         date__lte=month_end, date__gte=month_start)).order_by('-sum_transactions'))

    income_transactions = [[i['category__name'], round(i['sum_transactions'], 2)] for i in income_groupby]
    expense_groupby = list(Transaction.objects.values('category__name').annotate(sum_transactions=Sum('amount')).filter((Q(user=request.user) | Q(user=None)) &
                                                         Q(category__expense_or_income_choices='EXPENSE',
                                                         date__lte=month_end, date__gte=month_start)).order_by('-sum_transactions'))

    expense_transactions = [[i['category__name'], round(i['sum_transactions'], 2)] for i in expense_groupby]
    data = {
        'balance': income - expense,
        'income': income,
        'expense': expense,
        'income_transactions': income_transactions,
        'expense_transactions': expense_transactions
    }
    return JsonResponse(data)


def check_transactions(request):
    month = request.GET.get('month')
    year = int(request.GET.get('year'))
    month = int(month_name_to_number(month))
    month_range = calendar.monthrange(year, month)
    month_end = str(year)+'-'+str(month)+'-'+str(month_range[1])
    month_start = str(year)+'-'+str(month)+'-01'
    income = sum(Transaction.objects.filter((Q(user=request.user) | Q(user=None)) &
                                            Q(category__expense_or_income_choices='INCOME', date__lte=month_end,
                                              date__gte=month_start)).values_list('amount', flat=True))
    expense = sum(Transaction.objects.filter((Q(user=request.user) | Q(user=None)) &
                                             Q(category__expense_or_income_choices='EXPENSE', date__lte=month_end,
                                               date__gte=month_start)).values_list('amount', flat=True))
    income_transactions = list(Transaction.objects.filter((Q(user=request.user) | Q(user=None)) &
                                                Q(category__expense_or_income_choices='INCOME', date__lte=month_end,
                                                  date__gte=month_start)).values_list('pk', 'amount', 'category__name', 'date').order_by('-date'))

    expense_transactions = list(Transaction.objects.filter((Q(user=request.user) | Q(user=None)) &
                                                Q(category__expense_or_income_choices='EXPENSE', date__lte=month_end,
                                                  date__gte=month_start)).values_list('pk', 'amount', 'category__name', 'date').order_by('-date'))
    url_update_income_list = [reverse('update_income', args=(trans[0],)) for trans in income_transactions]
    url_update_expense_list = [reverse('update_expense', args=(trans[0],)) for trans in expense_transactions]
    url_delete_income_list = [reverse('delete_transaction', args=(trans[0],)) for trans in income_transactions]
    url_delete_expense_list = [reverse('delete_transaction', args=(trans[0],)) for trans in expense_transactions]
    data = {
        'balance': income - expense,
        'income': income,
        'expense': expense,
        'income_transactions': income_transactions,
        'expense_transactions': expense_transactions,
        'url_update_expense_list': url_update_expense_list,
        'url_update_income_list': url_update_income_list,
        'url_delete_expense_list': url_delete_expense_list,
        'url_delete_income_list': url_delete_income_list
    }

    return JsonResponse(data)
