from django.conf.urls import url
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from server.consumers import SocketConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                url(r"^systems/connect/(?P<host_name>[\w.@+-]+)/$", SocketConsumer.as_asgi()),
                url(r"^servers/connect/(?P<host_name>[\w.@+-]+)/$", SocketConsumer.as_asgi()),
                url(r"^tablets/connect/(?P<host_name>[\w.@+-]+)/$", SocketConsumer.as_asgi()),
            ]
        )
    )
})

