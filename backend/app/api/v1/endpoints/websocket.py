from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json
import asyncio
from app.core.redis_client import redis_client
from app.schemas.document import ProgressEvent

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.job_subscriptions = {}  # job_id -> list of connections

    async def connect(self, websocket: WebSocket, job_id: int = None):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        if job_id:
            if job_id not in self.job_subscriptions:
                self.job_subscriptions[job_id] = []
            self.job_subscriptions[job_id].append(websocket)

    def disconnect(self, websocket: WebSocket, job_id: int = None):
        self.active_connections.remove(websocket)
        
        if job_id and job_id in self.job_subscriptions:
            if websocket in self.job_subscriptions[job_id]:
                self.job_subscriptions[job_id].remove(websocket)
            if not self.job_subscriptions[job_id]:
                del self.job_subscriptions[job_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_job_subscribers(self, job_id: int, message: dict):
        if job_id in self.job_subscriptions:
            for connection in self.job_subscriptions[job_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    # Connection might be closed, remove it
                    self.disconnect(connection, job_id)

    async def broadcast_to_all(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Connection might be closed
                self.active_connections.remove(connection)


manager = ConnectionManager()


@router.websocket("/progress/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: int):
    await manager.connect(websocket, job_id)
    try:
        while True:
            # Keep connection alive and listen for any client messages
            data = await websocket.receive_text()
            # Echo back or handle client messages if needed
            await manager.send_personal_message(f"Echo: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket, job_id)


# Redis Pub/Sub listener for progress events
async def listen_to_progress_events():
    """Listen to Redis Pub/Sub for progress events and forward to WebSocket clients"""
    pubsub = redis_client.pubsub()
    pubsub.subscribe("job_progress")
    
    while True:
        try:
            message = pubsub.get_message(timeout=1.0)
            if message and message['type'] == 'message':
                data = json.loads(message['data'])
                job_id = data.get('job_id')
                
                # Forward to relevant WebSocket connections
                await manager.broadcast_to_job_subscribers(job_id, data)
                
        except Exception as e:
            print(f"Error in Redis listener: {e}")
            await asyncio.sleep(1)


# Start the Redis listener in the background
async def start_redis_listener():
    asyncio.create_task(listen_to_progress_events())
