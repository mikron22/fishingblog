# Generated by Django 2.2.6 on 2021-04-11 15:28

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210411_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='jpeg', keep_meta=True, null=True, quality=0, size=[800, 800], upload_to='images/', verbose_name='Zdjęcie (opcjonalne)'),
        ),
    ]
