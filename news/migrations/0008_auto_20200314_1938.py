# Generated by Django 2.2.8 on 2020-03-14 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20200126_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='artikull',
            name='hits',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='artikull',
            name='nga',
            field=models.IntegerField(choices=[(1, 'tvKlan'), (2, 'Faxweb'), (3, 'top-channel')], default=1),
        ),
    ]
