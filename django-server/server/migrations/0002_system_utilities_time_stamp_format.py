# Generated by Django 3.1.3 on 2020-11-12 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='system_utilities',
            name='time_stamp_format',
            field=models.TextField(default='SOME STRING', max_length=140),
        ),
    ]
