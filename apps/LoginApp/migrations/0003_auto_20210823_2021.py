# Generated by Django 3.1.5 on 2021-08-23 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoginApp', '0002_auto_20210601_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kvantuser',
            name='color',
            field=models.CharField(choices=[('orange', 'orange'), ('blue', 'blue')], default='blue', max_length=100),
        ),
        migrations.AlterField(
            model_name='kvantuser',
            name='theme',
            field=models.CharField(choices=[('dark', 'dark'), ('light', 'light')], default='light', max_length=100),
        ),
    ]