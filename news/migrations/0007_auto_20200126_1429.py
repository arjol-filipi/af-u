# Generated by Django 2.2.8 on 2020-01-26 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_comment_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikull',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
