#!/usr/bin/python3

import requests
import psutil
import datetime
import time


url = ''
host_name = psutil.users()[0].name
print(host_name)
headers = {'User-Agent': 'Mozilla/5.0'}
total_ram = float("{:.2f}".format(psutil.virtual_memory().total/1024/1000000))
while True:
    used_ram = float("{:.2f}".format(
        psutil.virtual_memory().used/1024/1000000))
    ram_percent = float("{:.2f}".format((used_ram/total_ram)*100))
    cpu_usage = str(psutil.cpu_percent(interval=1))+"%"
    print(cpu_usage)
    ram_usage = str(used_ram) + " GB out of " + \
        str(total_ram) + " GB (" + str(ram_percent)+"% )"
    total_disk = float("{:.2f}".format(
        psutil.disk_usage('/').total/1000000000))
    used_disk = float("{:.2f}".format(psutil.disk_usage('/').used/1000000000))
    disk_percent = float("{:.2f}".format(psutil.disk_usage('/').percent))
    disk_usage = str(used_disk) + " GB out of " + \
        str(total_disk) + " GB (" + str(disk_percent) + "%)"
    print(disk_usage)
    current_time = datetime.datetime.now().strftime("%d-%b-%Y %I:%M %p")
    time_ = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    dictionary = {"host_name": host_name, "cpu_usage": cpu_usage, "ram_usage": ram_usage,
                  "disk_usage": disk_usage, "current_time": current_time, "time_": time_}
    try:
        x = requests.post(url, data=dictionary, headers=headers)
    except:
        print("Connection refused")
    time.sleep(5)
