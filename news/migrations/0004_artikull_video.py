# Generated by Django 2.2.8 on 2020-01-25 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20200124_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='artikull',
            name='video',
            field=models.BooleanField(default=False),
        ),
    ]