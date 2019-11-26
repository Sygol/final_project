# Generated by Django 2.2.7 on 2019-11-26 12:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Category name')),
                ('is_income_category', models.BooleanField(verbose_name='Is income category')),
                ('created', models.DateTimeField(default=datetime.datetime(2019, 11, 26, 12, 37, 50, 390365, tzinfo=utc), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2019, 11, 26, 12, 37, 50, 390365, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='UserCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Category name')),
                ('is_income_category', models.BooleanField(verbose_name='Is income category')),
                ('created', models.DateTimeField(default=datetime.datetime(2019, 11, 26, 12, 37, 50, 391364, tzinfo=utc), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2019, 11, 26, 12, 37, 50, 391364, tzinfo=utc))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_categories', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('date', models.DateField(verbose_name='Date')),
                ('created', models.DateTimeField(default=datetime.datetime(2019, 11, 26, 12, 37, 50, 393363, tzinfo=utc), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2019, 11, 26, 12, 37, 50, 393363, tzinfo=utc))),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to='money_tracker.Category', verbose_name='Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('user_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to='money_tracker.UserCategory', verbose_name='User category')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('date', models.DateField(verbose_name='Date')),
                ('created', models.DateTimeField(default=datetime.datetime(2019, 11, 26, 12, 37, 50, 392365, tzinfo=utc), editable=False)),
                ('modified', models.DateTimeField(default=datetime.datetime(2019, 11, 26, 12, 37, 50, 392365, tzinfo=utc))),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='money_tracker.Category', verbose_name='Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('user_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='money_tracker.UserCategory', verbose_name='User category')),
            ],
        ),
    ]