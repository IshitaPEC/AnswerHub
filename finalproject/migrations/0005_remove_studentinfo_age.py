# Generated by Django 3.2.9 on 2021-11-26 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finalproject', '0004_auto_20211126_0608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentinfo',
            name='age',
        ),
    ]
