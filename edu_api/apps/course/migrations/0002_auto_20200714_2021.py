# Generated by Django 2.0.6 on 2020-07-14 12:21

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_video',
            field=models.FileField(blank=True, null=True, upload_to='video', verbose_name='视频'),
        ),
        migrations.AlterField(
            model_name='course',
            name='brief',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=2048, null=True, verbose_name='详情介绍'),
        ),
    ]
