# Generated by Django 2.2.7 on 2019-11-26 16:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20191126_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 26, 16, 7, 1, 655630, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 26, 16, 7, 1, 655630, tzinfo=utc)),
        ),
    ]
