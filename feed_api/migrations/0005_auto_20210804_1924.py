# Generated by Django 3.2.5 on 2021-08-04 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feed_api', '0004_image_post_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_image', to='feed_api.comment')),
            ],
        ),
        migrations.CreateModel(
            name='FeedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feed_image', to='feed_api.feed')),
            ],
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]