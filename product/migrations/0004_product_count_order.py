# Generated by Django 3.2.6 on 2021-11-20 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20211026_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count_order',
            field=models.BigIntegerField(default=0),
        ),
    ]
