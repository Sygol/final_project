from django import forms

from money_tracker.models import UserCategory


class UserCategoryForm(forms.ModelForm):

    class Meta:
        model = UserCategory
        fields = ['expense_or_income_choices', 'name']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        cat = UserCategory.objects.create(user=self.request.user, name=self.cleaned_data.get('name'),
                                          expense_or_income_choices=self.cleaned_data.get('expense_or_income_choices'))
        return cat
