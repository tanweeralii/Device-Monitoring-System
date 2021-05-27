from django.db import models

class system_Utilities_Systems(models.Model):

    u_name = models.TextField()

    ram_usage = models.TextField()

    cpu_usage = models.TextField()

    disk_usage = models.TextField()

    time_stamp = models.TextField()

    time_stamp_format = models.TextField(max_length=140, default='SOME STRING')

    teamviewer_id = models.TextField(default='Not Applied');

    anydesk_id = models.TextField(default='Not Applied');

class system_Utilities_Servers(models.Model):
    
    u_name = models.TextField()

    server_type = models.TextField()

    ram_usage = models.TextField()

    cpu_usage = models.TextField()

    disk_usage = models.TextField()

    time_stamp = models.TextField()

    time_stamp_format = models.TextField(max_length=140, default='SOME STRING')

    teamviewer_id = models.TextField(default='Not Applied');

    anydesk_id = models.TextField(default='Not Applied');


class system_Utilities_Tablets(models.Model):
            
    u_name = models.TextField()

    ram_usage = models.TextField()

    cpu_usage = models.TextField()

    disk_usage = models.TextField()

    time_stamp = models.TextField()

    time_stamp_format = models.TextField(max_length=140, default='SOME STRING')

