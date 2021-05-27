"""asset_monitoring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from server import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", views.Login.as_view(), name='login'),
    path("logout/", views.Logout.as_view(), name='logout'),
    path("", views.Select_Device.as_view(), name='select_device'),
    path("systems/", views.Systems.as_view(), name='systems'),
    path("servers/", views.Servers.as_view(), name='servers'),
    path("tablets/", views.Tablets.as_view(), name='tablets'),
    path("postsystems/",csrf_exempt(views.post_request_systems)),
    path("posttablets/",csrf_exempt(views.post_request_tablets)),
    path("postservers/",csrf_exempt(views.post_request_servers)),
    path("systems/connect/<str:host_name>/", views.connectwindowssystems),
    path("servers/connect/<str:host_name>/", views.connectlinux),
    path("tablets/connect/<str:host_name>/", views.connecttablets),
    path("addsystem", csrf_exempt(views.addsystem)),
    path("addserver", csrf_exempt(views.addserver)),
    path("addtablet", csrf_exempt(views.addtablet)),
    path("remsystem", csrf_exempt(views.remsystem)),
    path("remserver", csrf_exempt(views.remserver)),
    path("remtablet", csrf_exempt(views.remtablet)),
    path("download/<str:host_name>/", csrf_exempt(views.download)),
]
