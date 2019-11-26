from django.contrib import admin

# Register your models here.
from money_tracker.models import Category, UserCategory, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'expense_or_income_choices', 'created', 'modified']
    exclude = ('modified',)


@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'expense_or_income_choices', 'created', 'modified']
    exclude = ('modified',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'user_category', 'user', 'amount', 'date', 'created', 'modified']
    exclude = ('modified',)
