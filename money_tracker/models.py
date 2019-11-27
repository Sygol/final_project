from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
from accounts.models import CustomUser


class Category(models.Model):
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'
    EXPENSE_OR_INCOME_CHOICES = [
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'),
    ]

    name = models.CharField(max_length=32, verbose_name=_('Category name'))
    user = models.ForeignKey('accounts.CustomUser', related_name='user_categories', on_delete=models.CASCADE,
                             verbose_name=_('User'), null=True, blank=True)
    expense_or_income_choices = models.CharField(max_length=9, choices=EXPENSE_OR_INCOME_CHOICES,
                                                 verbose_name=_('Expense or income'), default=EXPENSE)
    created = models.DateTimeField(editable=False, default=timezone.now())
    modified = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Category, self).save(*args, **kwargs)


# class UserCategory(models.Model):
#     INCOME = 'INCOME'
#     EXPENSE = 'EXPENSE'
#     EXPENSE_OR_INCOME_CHOICES = [
#         (INCOME, 'Income'),
#         (EXPENSE, 'Expense'),
#     ]
#     name = models.CharField(max_length=32, verbose_name=_('Category name'))
#     user = models.ForeignKey('accounts.CustomUser', related_name='user_categories', on_delete=models.CASCADE, verbose_name=_('User'))
#     expense_or_income_choices = models.CharField(max_length=9, choices=EXPENSE_OR_INCOME_CHOICES,
#                                                  verbose_name=_('Expense or income'), default=EXPENSE)
#     created = models.DateTimeField(editable=False, default=timezone.now())
#     modified = models.DateTimeField(default=timezone.now())
#
#     def __str__(self):
#         return f'{self.name}'
#
#     def save(self, *args, **kwargs):
#         if not self.id:
#             self.created = timezone.now()
#         self.modified = timezone.now()
#         return super(UserCategory, self).save(*args, **kwargs)


class Transaction(models.Model):
    category = models.ForeignKey('money_tracker.Category', related_name='transactions', on_delete=models.CASCADE,
                                 verbose_name=_('Category'), null=True, blank=True)
    user = models.ForeignKey('accounts.CustomUser', related_name='transactions', on_delete=models.CASCADE,
                             verbose_name=_('User'))
    amount = models.DecimalField(verbose_name=_('Amount'), max_digits=10, decimal_places=2)
    date = models.DateField(verbose_name=_('Date'))
    created = models.DateTimeField(editable=False, default=timezone.now())
    modified = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f'{self.category} - {self.user} - {self.amount}({self.date})'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Transaction, self).save(*args, **kwargs)
