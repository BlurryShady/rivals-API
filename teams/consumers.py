import json

from channels.generic.websocket import AsyncWebsocketConsumer


class TeamCommentConsumer(AsyncWebsocketConsumer):
    """Broadcast new comments for a specific team in real time."""

    async def connect(self):
        self.slug = self.scope["url_route"]["kwargs"]["slug"]
        self.group_name = f"team_comments_{self.slug}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        # Clients post comments via REST; ignore inbound websocket payloads.
        return

    async def comment_broadcast(self, event):
        await self.send(text_data=json.dumps(event["comment"]))
