# Generated by Django 3.2.6 on 2021-12-12 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20211212_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='bin',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='company',
            name='fio',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='type_price',
            field=models.SmallIntegerField(blank=True, choices=[(1, 'Розничный'), (2, 'Оптовый'), (3, 'Спец.цена')], null=True),
        ),
    ]