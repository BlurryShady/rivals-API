from django.urls import re_path

from .consumers import TeamCommentConsumer

websocket_urlpatterns = [
    re_path(
        r"ws/teams/(?P<slug>[\w-]+)/comments/",
        TeamCommentConsumer.as_asgi(),
    ),
]
