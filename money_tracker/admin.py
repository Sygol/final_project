from django.contrib import admin

# Register your models here.
from money_tracker.models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'expense_or_income_choices', 'created', 'modified']
    exclude = ('modified',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'user', 'amount', 'date', 'created', 'modified']
    exclude = ('modified',)
