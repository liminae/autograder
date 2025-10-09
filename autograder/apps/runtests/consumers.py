import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)


class SubmissionStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_group_name = f"user_{self.scope['user'].id}"

        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "join_submissions":
            submission_ids = data["submission_ids"]
            for submission_id in submission_ids:
                group_name = f"submission_{submission_id}"
                await self.channel_layer.group_add(group_name, self.channel_name)
                logger.info(f"Added client to group {group_name}")

    async def submission_status(self, event):
        message = event["message"]
        runtime = event["runtime"]
        submission_id = event["submission_id"]
        await self.send(
            text_data=json.dumps(
                {"submission_id": submission_id, "message": message, "runtime": runtime}
            )
        )
