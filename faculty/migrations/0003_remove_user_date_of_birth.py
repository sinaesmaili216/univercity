# Generated by Django 3.2.7 on 2021-09-01 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0002_auto_20210901_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_of_birth',
        ),
    ]
