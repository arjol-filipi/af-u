# Generated by Django 2.2.8 on 2020-01-30 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ans',
            name='hint',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Clue',
        ),
    ]