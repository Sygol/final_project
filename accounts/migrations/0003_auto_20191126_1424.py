# Generated by Django 2.2.7 on 2019-11-26 13:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20191126_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 26, 13, 24, 52, 439135, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 26, 13, 24, 52, 439135, tzinfo=utc)),
        ),
    ]