# Generated by Django 2.2.8 on 2020-02-02 13:48

from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('cw', '0004_lead_hint'),
    ]

    operations = [
        migrations.AddField(
            model_name='crossword',
            name='published',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime.now()),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lead',
            name='pos',
            field=models.CharField(default='1', max_length=3),
            preserve_default=False,
        ),
    ]
