# Generated by Django 3.2.5 on 2021-08-10 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed_api', '0005_auto_20210804_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='like', to='feed_api.comment')),
                ('feed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='like', to='feed_api.feed')),
            ],
        ),
        migrations.DeleteModel(
            name='CommentImage',
        ),
    ]
