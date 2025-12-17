import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)


class TeamCommentConsumer(AsyncWebsocketConsumer):
    """Broadcast new comments for a specific team in real time."""

    async def connect(self):
        self.slug = self.scope["url_route"]["kwargs"]["slug"]
        self.group_name = f"team_comments_{self.slug}"

        await self.accept()

        # This will eliminate errors if Redis is not configured
        if not self.channel_layer:
            logger.warning("No channel_layer configured; websocket will be passive.")
            return

        try:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
        except Exception:
            logger.exception("group_add failed; websocket will be passive.")
            return

    async def disconnect(self, close_code):
        if not self.channel_layer:
            return

        try:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        except Exception:
            logger.exception("group_discard failed.")

    async def receive(self, text_data=None, bytes_data=None):
        # Clients post comments via REST. Ignore inbound websocket payloads
        return

    async def comment_broadcast(self, event):
        await self.send(text_data=json.dumps(event["comment"]))
