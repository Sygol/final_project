import datetime

from django import forms
from django.db.models import Q
from django.forms import DateInput

from money_tracker.models import Transaction, Category


class UserCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['expense_or_income_choices', 'name']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        cat = Category.objects.create(user=self.request.user, name=self.cleaned_data.get('name'),
                                      expense_or_income_choices=self.cleaned_data.get('expense_or_income_choices'))
        return cat


class UserExpensesForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=True)

    class Meta:
        model = Transaction
        fields = ['amount', 'date']
        widgets = {
            'date': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(Q(user=self.request.user,
                                expense_or_income_choices='EXPENSE') | Q(user=None, expense_or_income_choices='EXPENSE'))

    def save(self, commit=True):
        transaction = Transaction.objects.create(user=self.request.user, category=self.cleaned_data.get('category'),
                                                 amount=self.cleaned_data.get('amount'), date=self.cleaned_data.get('date'))
        return transaction

