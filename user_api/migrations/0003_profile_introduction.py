# Generated by Django 3.2.6 on 2021-09-10 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_api', '0002_remove_profile_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='introduction',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
