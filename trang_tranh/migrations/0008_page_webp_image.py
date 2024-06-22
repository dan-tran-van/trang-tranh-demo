# Generated by Django 4.2.13 on 2024-06-22 06:26

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('trang_tranh', '0007_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='webp_image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='WEBP', keep_meta=True, null=True, quality=75, scale=None, size=[1920, 1080], upload_to='webp-page-images/', verbose_name='webp image'),
        ),
    ]
