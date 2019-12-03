import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import DateInput
from django.urls import reverse

from money_tracker.models import Transaction, Category


class UserCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['expense_or_income_choices', 'name']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(name__iexact=name, user=self.request.user,
                                   expense_or_income_choices=self.cleaned_data['expense_or_income_choices']).exists() or\
                Category.objects.filter(name=name, user=None,
                                    expense_or_income_choices=self.cleaned_data['expense_or_income_choices']).exists():
            raise ValidationError('This category already exists!')
        return name

    def save(self, commit=True):
        cat = Category.objects.create(user=self.request.user, name=self.cleaned_data.get('name').capitalize(),
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
        self.is_object_created = kwargs['instance']
        self.fields['category'].queryset = Category.objects.filter(Q(user=self.request.user,
                               expense_or_income_choices='EXPENSE') | Q(user=None, expense_or_income_choices='EXPENSE'))

    def save(self, commit=True):

        if not self.is_object_created:
            transaction = Transaction.objects.create(user=self.request.user, category=self.cleaned_data.get('category'),
                                                     amount=self.cleaned_data.get('amount'), date=self.cleaned_data.get('date'))
            return transaction
        else:
            Transaction.objects.filter(id=self.is_object_created.id).update(amount=self.cleaned_data.get('amount'),
                                                                            date=self.cleaned_data.get('date'),
                                                                            category=self.cleaned_data.get('category'))
            return Transaction.objects.filter(id=self.is_object_created.id)


class UserIncomeForm(forms.ModelForm):
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
        self.fields['category'].queryset = Category.objects.filter((Q(user=self.request.user) | Q(user=None)) &
                                                                   Q(expense_or_income_choices='INCOME'))

    def save(self, commit=True):
        transaction = Transaction.objects.create(user=self.request.user, category=self.cleaned_data.get('category'),
                                                 amount=self.cleaned_data.get('amount'), date=self.cleaned_data.get('date'))
        return transaction


class UserTransactionForm(forms.ModelForm):
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
        self.is_object_created = kwargs['instance']
        try:
            if self.request.get_full_path() == reverse('add_income') or \
                    self.request.get_full_path() == reverse('update_income', kwargs={'pk': self.is_object_created.id}):
                self.fields['category'].queryset = Category.objects.filter(Q(user=self.request.user,
                                   expense_or_income_choices='INCOME') | Q(user=None, expense_or_income_choices='INCOME'))
            elif self.request.get_full_path() == reverse('add_expense') or \
                    self.request.get_full_path() == reverse('update_expense', kwargs={'pk': self.is_object_created.id}):
                self.fields['category'].queryset = Category.objects.filter(Q(user=self.request.user,
                                   expense_or_income_choices='EXPENSE') | Q(user=None, expense_or_income_choices='EXPENSE'))
        except AttributeError:
            self.fields['category'].queryset = Category.objects.filter(Q(user=self.request.user,
                                                                         expense_or_income_choices='EXPENSE') | Q(
                                                                        user=None, expense_or_income_choices='EXPENSE'))

    def save(self, commit=True):

        if not self.is_object_created:
            transaction = Transaction.objects.create(user=self.request.user, category=self.cleaned_data.get('category'),
                                                     amount=self.cleaned_data.get('amount'), date=self.cleaned_data.get('date'))
            return transaction
        else:
            Transaction.objects.filter(id=self.is_object_created.id).update(amount=self.cleaned_data.get('amount'),
                                                                            date=self.cleaned_data.get('date'),
                                                                            category=self.cleaned_data.get('category'))
            return Transaction.objects.filter(id=self.is_object_created.id)