# Generated by Django 3.1.5 on 2021-03-29 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kvantlesson',
            name='time',
            field=models.TimeField(default=None),
        ),
    ]
