# Generated by Django 3.2.6 on 2021-12-08 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20211208_1530'),
        ('product', '0004_product_count_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.company'),
        ),
    ]
