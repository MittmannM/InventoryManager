# Generated by Django 3.2.13 on 2022-04-29 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invmanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='quantity',
            field=models.IntegerField(default=1, verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='machinery',
            name='machinery_number',
            field=models.IntegerField(verbose_name='Number'),
        ),
    ]
