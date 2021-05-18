# Generated by Django 3.1.5 on 2021-05-16 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MailApp', '0007_auto_20210516_0842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kvantmessage',
            name='is_read',
        ),
        migrations.CreateModel(
            name='MailReceiver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='kvantmessage',
            name='receivers',
            field=models.ManyToManyField(related_name='receivers', to='MailApp.MailReceiver'),
        ),
    ]