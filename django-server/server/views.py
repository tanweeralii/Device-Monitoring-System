from boto3.session import Session
from django.http import FileResponse
from django.contrib import messages
from django.http import HttpResponseRedirect,JsonResponse
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.conf import settings
from server.models import system_Utilities_Systems, system_Utilities_Servers, system_Utilities_Tablets



class Systems(View):
    templates = 'systems.html'

    def get(self, request):
        system_util = system_Utilities_Systems.objects
        context = {"url": settings.IP_ADDRESS, "util": system_util}
        if request.user.is_authenticated:
            return render(request, self.templates, context)
        else:
            return redirect('/login/')


class Servers(View):
    templates = 'servers.html'

    def get(self, request):
        try:
            system_util_linux = system_Utilities_Servers.objects.filter(server_type='linux')
        except:
            system_util_linux = None;
        try:
            system_util_windows = system_Utilities_Servers.objects.filter(server_type='windows')
        except:
            system_util_windows = None;
        context = {"url": settings.IP_ADDRESS, "linux": system_util_linux, "windows": system_util_windows}
        if request.user.is_authenticated:
            return render(request, self.templates, context)
        else:
            return redirect('/login/')


class Tablets(View):
    templates = 'tablets.html'

    def get(self, request):
        system_util = system_Utilities_Tablets.objects
        context = {"url": settings.IP_ADDRESS, "util": system_util}
        if request.user.is_authenticated:
            return render(request, self.templates, context)
        else:
            return redirect('/login/')

def download(request, host_name):
    session = Session(aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY)
    s3 = session.resource('s3')
    my_bucket = s3.Bucket(settings.BUCKET_NAME)
    for s3_files in my_bucket.objects.all():
        print(s3_files.key)
    file_name = host_name + '.txt'
    my_bucket.download_file(file_name,'./server/static/downloads/'+file_name)
    response = FileResponse(open('./server/static/downloads/'+file_name, 'rb'))
    return response

def post_request_systems(request):
    p=system_Utilities_Systems.objects.get(u_name=request.POST["host_name"])
    p.u_name = request.POST["host_name"]
    p.ram_usage = request.POST["ram_usage"]
    p.disk_usage = request.POST["disk_usage"]
    p.cpu_usage = request.POST["cpu_usage"]
    p.time_stamp = request.POST["current_time"]
    p.time_stamp_format = request.POST["time_"]
    p.save()
    return render(request, "post.html")


def post_request_servers(request):
    p=system_Utilities_Servers.objects.get(u_name=request.POST["host_name"])
    p.u_name = request.POST["host_name"]
    p.ram_usage = request.POST["ram_usage"]
    p.disk_usage = request.POST["disk_usage"]
    p.cpu_usage = request.POST["cpu_usage"]
    p.time_stamp = request.POST["current_time"]
    p.time_stamp_format = request.POST["time_"]
    p.save()
    return render(request, "post.html")

def post_request_tablets(request):
    print(request.POST)
    p=system_Utilities_Tablets.objects.get(u_name=request.POST["host_name"])
    p.u_name = request.POST["host_name"]
    p.ram_usage = request.POST["ram_usage"]
    p.disk_usage = request.POST["disk_usage"]
    p.cpu_usage = request.POST["cpu_usage"]
    p.time_stamp = request.POST["current_time"]
    p.time_stamp_format = request.POST["time_"]
    p.save()
    return render(request, "post.html")


class Select_Device(View):
    templates = 'select.html'

    def get(self, request):
        context = {"url": settings.IP_ADDRESS}
        if request.user.is_authenticated:
            return render(request, self.templates, context)
        else:
            return redirect('/login/')


def connectwindowssystems(request, host_name):
        p = system_Utilities_Systems.objects.get(u_name=host_name)
        context = {"host_name":host_name,"topic":"Monitor Systems","urll":"systems","teamviewer_id":p.teamviewer_id, "anydesk_id":p.anydesk_id}
        if request.user.is_authenticated:
            return render(request, "connect_windows.html", context)
        else:
            return redirect('/login/')


def connectlinux(request, host_name):
        p = system_Utilities_Servers.objects.get(u_name=host_name)
        context = {"host_name":host_name,"teamviewer_id":p.teamviewer_id,"anydesk_id":p.anydesk_id}
        if request.user.is_authenticated:
            return render(request, "connect_linux.html", context)
        else:
            return redirect('/login/')

def connecttablets(request, host_name):
        context= {"host_name":host_name,"urll":"tablets","topic":"Monitor Tablets"}
        if request.user.is_authenticated:
            return render(request, "connect_tablets.html", context)
        else:
            return redirect('/login/')

def addsystem(request):
    print(request.POST['data'])
    p=system_Utilities_Systems.objects.filter(u_name=request.POST["data"]).exists()
    print(p)
    if p is True:
        return JsonResponse({'message':'Host Name already exists'})
    else:
        if request.POST["teamviewer_id"] is "" and request.POST["anydesk_id"] is "":
            p = system_Utilities_Systems(u_name=request.POST["data"],ram_usage="Not Applied",disk_usage="Not Applied",cpu_usage="Not Applied",time_stamp="Not Applied",time_stamp_format="Not Applied",teamviewer_id="Not Applied",anydesk_id="Not Applied");
        elif request.POST["anydesk_id"] is "":
             p = system_Utilities_Systems(u_name=request.POST["data"],ram_usage="Not Applied",disk_usage="Not Applied",cpu_usage="Not Applied",time_stamp="Not Applied",time_stamp_format="Not Applied",teamviewer_id=request.POST["teamviewer_id"],anydesk_id="Not Applied");
        elif request.POST["teamviewer_id"] is "":
            p = system_Utilities_Systems(u_name=request.POST["data"],ram_usage="Not Applied",disk_usage="Not Applied",cpu_usage="Not Applied",time_stamp="Not Applied",time_stamp_format="Not Applied",teamviewer_id="Not Applied",anydesk_id=request.POST["anydesk_id"]);
        else:
            p = system_Utilities_Systems(u_name=request.POST["data"],ram_usage="Not Applied",disk_usage="Not Applied",cpu_usage="Not Applied",time_stamp="Not Applied",time_stamp_format="Not Applied",teamviewer_id=request.POST["teamviewer_id"],anydesk_id=request.POST["anydesk_id"]);
        p.save();
        return JsonResponse({'message':'Host Added Successfully'})


def addserver(request):
    print(request.POST['data'])
    p=system_Utilities_Servers.objects.filter(u_name=request.POST["data"]).exists()
    print(p)
    if p is True:
        return JsonResponse({'message':'Host Name already exists'})
    else:
        if request.POST["teamviewer_id"] is "" and request.POST["anydesk_id"] is "":
            p = system_Utilities_Servers(u_name=request.POST["data"],ram_usage="Not Applied",disk_usage="Not Applied",cpu_usage="Not Applied",time_stamp="Not Applied",time_stamp_format="Not Applied",teamviewer_id="Not Applied",anydesk_id="Not Applied", server_type=request.POST["server_type"]);
        elif request.POST["teamviewer_id"] is "":
             p = system_Utilities_Servers(u_name=request.POST["data"],ram_usage="Not Applied",disk_usage="Not Applied",cpu_usage="Not Applied",time_stamp="Not Applied",time_stamp_format="Not Applied", teamviewer_id="Not Applied",anydesk_id=request.POST["anydesk_id"], server_type=request.POST["server_type"]);
        elif request.POST["anydesk_id"] is "":
             p = system_Utilities_Servers(u_name=request.POST["data"],ram_usage="Not Applied",disk_usage="Not Applied",cpu_usage="Not Applied",time_stamp="Not Applied",time_stamp_format="Not Applied", teamviewer_id=request.POST["teamviewer_id"],anydesk_id="Not Applied", server_type=request.POST["server_type"]);
        else:
             p = system_Utilities_Servers(u_name=request.POST["data"],ram_usage="Not Applied",disk_usage="Not Applied",cpu_usage="Not Applied",time_stamp="Not Applied",time_stamp_format="Not Applied", teamviewer_id=request.POST["teamviewer_id"],anydesk_id=request.POST["anydesk_id"], server_type=request.POST["server_type"]);
        p.save();
        return JsonResponse({'message':'Host Added Successfully'})


def addtablet(request):
    print(request.POST['data'])
    p=system_Utilities_Tablets.objects.filter(u_name=request.POST["data"]).exists()
    print(p)
    if p is True:
        return JsonResponse({'message':'Host Name already exists'})
    else:
        p = system_Utilities_Tablets(u_name=request.POST["data"],ram_usage="Not Applied",disk_usage="Not Applied",cpu_usage="Not Applied",time_stamp="Not Applied",time_stamp_format="Not Applied");
        p.save();
        return JsonResponse({'message':'Host Added Successfully'})


def remsystem(request):
    print(request.POST['data'])
    p=system_Utilities_Systems.objects.filter(u_name=request.POST["data"]).exists()
    print(p)
    if p is False:
        return JsonResponse({'message':'Host Name Does not exist'});
    else:
        q = system_Utilities_Systems.objects.filter(u_name=request.POST["data"]).delete()
        return JsonResponse({'message':'Host Removed Successfully'})

def remserver(request):
    print(request.POST['data'])
    p=system_Utilities_Servers.objects.filter(u_name=request.POST["data"]).exists()
    print(p)
    if p is False:
        return JsonResponse({'message':'Host Name Does not exist'});
    else:
        q = system_Utilities_Servers.objects.filter(u_name=request.POST["data"]).delete()
        return JsonResponse({'message':'Host Removed Successfully'})

def remtablet(request):
    print(request.POST['data'])
    p=system_Utilities_Tablets.objects.filter(u_name=request.POST["data"]).exists()
    print(p)
    if p is False:
        return JsonResponse({'message':'Host Name Does not exist'});
    else:
        q = system_Utilities_Tablets.objects.filter(u_name=request.POST["data"]).delete()
        return JsonResponse({'message':'Host Removed Successfully'})


class Logout(View):
    templates='login.html'

    def get(self, request):
        if request.user.is_authenticated:
            logout(request) 
            return redirect('/login/')
        else:
            return redirect('/login/')

class Login(View):
    templates = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.templates, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request,'username or password not correct')
            return redirect('/login')

