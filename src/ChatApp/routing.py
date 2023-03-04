from django.urls import re_path
from . import consumers

# код используется для создания URL-адресов для веб-сокетов Django, а также для привязки соответствующих потребителей.

websocket_urlpatterns = [
    re_path(r'chat/(?P<project_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
