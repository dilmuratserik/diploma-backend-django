# Generated by Django 3.2.6 on 2021-09-27 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_sucategory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SuCategory',
            new_name='SubCategory',
        ),
    ]
