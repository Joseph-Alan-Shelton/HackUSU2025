import asyncio
import base64
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from . import mat2  # Import main from mat2
class LiveGraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.keep_running = True

        while self.keep_running:
            image_path = "static/images/graph.png"
            if os.path.exists(image_path):
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode("utf-8")
                
                await self.send(text_data=f"{image_data}")  # Send Base64

            await asyncio.sleep(1)  # Update every second

    async def disconnect(self, close_code):
        self.keep_running = False
