# Generated by Django 3.2.8 on 2021-11-16 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20211115_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='serviceDate',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
