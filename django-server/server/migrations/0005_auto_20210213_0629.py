# Generated by Django 3.1.3 on 2021-02-13 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_auto_20210114_1853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='system_utilities_desktops',
            old_name='remote_application',
            new_name='anydesk_id',
        ),
        migrations.RenameField(
            model_name='system_utilities_desktops',
            old_name='remote_id',
            new_name='teamviewer_id',
        ),
        migrations.RenameField(
            model_name='system_utilities_laptops',
            old_name='remote_application',
            new_name='anydesk_id',
        ),
        migrations.RenameField(
            model_name='system_utilities_laptops',
            old_name='remote_id',
            new_name='teamviewer_id',
        ),
        migrations.RenameField(
            model_name='system_utilities_servers',
            old_name='remote_application',
            new_name='anydesk_id',
        ),
        migrations.RenameField(
            model_name='system_utilities_servers',
            old_name='remote_id',
            new_name='teamviewer_id',
        ),
    ]
