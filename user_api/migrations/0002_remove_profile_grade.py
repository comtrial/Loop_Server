# Generated by Django 3.2.5 on 2021-09-10 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='grade',
        ),
    ]