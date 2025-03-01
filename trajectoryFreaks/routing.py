from django.urls import re_path
from .consumers import LiveGraphConsumer

websocket_urlpatterns = [
    re_path(r"ws/live-graph/$", LiveGraphConsumer.as_asgi()),
]
