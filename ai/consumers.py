
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from celery.result import AsyncResult
import json

class TaskProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        # expect message with {"task_id": "..."} or path contains it
        try:
            data = json.loads(text_data or "{}")
            task_id = data.get("task_id") or self.scope['url_route']['kwargs'].get('task_id')
        except Exception:
            await self.send_json({"error": "invalid payload"})
            return
        if not task_id:
            await self.send_json({"error": "task_id required"})
            return
        # poll celery result
        tries = 0
        while True:
            res = AsyncResult(task_id)
            state = res.state
            payload = {"state": state}
            if res.successful():
                payload["result"] = res.result
                await self.send_json(payload)
                break
            elif res.failed():
                payload["error"] = str(res.result or res.traceback or res._cache_version)
                await self.send_json(payload)
                break
            else:
                # still running or pending
                await self.send_json(payload)
                await asyncio.sleep(1.5)
                tries += 1
                if tries > 600:  # ~15 minutes
                    await self.send_json({"state":"TIMEOUT"})
                    break
