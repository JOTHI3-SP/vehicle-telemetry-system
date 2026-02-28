from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas
from .database import get_db
from .websocket import manager

router = APIRouter(prefix="/api")

@router.post("/telemetry", response_model=schemas.TelemetryResponse, status_code=201)
async def create_telemetry(
    telemetry: schemas.TelemetryCreate,
    db: Session = Depends(get_db)
):
    result = crud.create_telemetry(db, telemetry)
    
    # Broadcast to WebSocket subscribers
    await manager.broadcast({
        "id": result.id,
        "vehicleId": result.vehicleId,
        "speed": result.speed,
        "engineTemperature": result.engineTemperature,
        "batteryLevel": result.batteryLevel,
        "energyConsumption": result.energyConsumption,
        "latitude": result.latitude,
        "longitude": result.longitude,
        "timestamp": result.timestamp.isoformat(),
        "status": result.status
    }, result.vehicleId)
    
    return result

@router.get("/telemetry/{vehicle_id}/latest", response_model=schemas.TelemetryResponse)
def get_latest_telemetry(vehicle_id: str, db: Session = Depends(get_db)):
    telemetry = crud.get_latest_telemetry(db, vehicle_id)
    if not telemetry:
        raise HTTPException(status_code=404, detail="No telemetry found for vehicle")
    return telemetry

@router.get("/telemetry/{vehicle_id}", response_model=List[schemas.TelemetryResponse])
def get_telemetry_history(
    vehicle_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return crud.get_telemetry_history(db, vehicle_id, limit)

@router.websocket("/telemetry/stream")
async def telemetry_stream_all(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/telemetry/stream/{vehicle_id}")
async def telemetry_stream_vehicle(websocket: WebSocket, vehicle_id: str):
    await manager.connect(websocket, vehicle_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, vehicle_id)
