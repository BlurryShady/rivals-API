from teams import routing as teams_routing

websocket_urlpatterns = [
    *teams_routing.websocket_urlpatterns,
]
