from fastapi import WebSocket
from typing import List, Dict
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, vehicle_id: str = None):
        await websocket.accept()
        key = vehicle_id or "all"
        if key not in self.active_connections:
            self.active_connections[key] = []
        self.active_connections[key].append(websocket)
    
    def disconnect(self, websocket: WebSocket, vehicle_id: str = None):
        key = vehicle_id or "all"
        if key in self.active_connections:
            self.active_connections[key].remove(websocket)
    
    async def broadcast(self, message: dict, vehicle_id: str):
        # Send to vehicle-specific subscribers
        if vehicle_id in self.active_connections:
            for connection in self.active_connections[vehicle_id]:
                await connection.send_json(message)
        
        # Send to all subscribers
        if "all" in self.active_connections:
            for connection in self.active_connections["all"]:
                await connection.send_json(message)

manager = ConnectionManager()
