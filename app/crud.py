from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

def compute_status(speed: float, engine_temp: float, battery_level: float) -> str:
    if engine_temp > 120 or battery_level < 10:
        return "CRITICAL"
    if speed > 150:
        return "WARNING"
    return "NORMAL"

def create_telemetry(db: Session, telemetry: schemas.TelemetryCreate):
    timestamp = telemetry.timestamp or datetime.utcnow()
    status = compute_status(
        telemetry.speed,
        telemetry.engineTemperature,
        telemetry.batteryLevel
    )
    
    db_telemetry = models.Telemetry(
        vehicleId=telemetry.vehicleId,
        speed=telemetry.speed,
        engineTemperature=telemetry.engineTemperature,
        batteryLevel=telemetry.batteryLevel,
        energyConsumption=telemetry.energyConsumption,
        latitude=telemetry.latitude,
        longitude=telemetry.longitude,
        timestamp=timestamp,
        status=status
    )
    db.add(db_telemetry)
    db.commit()
    db.refresh(db_telemetry)
    return db_telemetry

def get_latest_telemetry(db: Session, vehicle_id: str):
    return db.query(models.Telemetry).filter(
        models.Telemetry.vehicleId == vehicle_id
    ).order_by(models.Telemetry.timestamp.desc()).first()

def get_telemetry_history(db: Session, vehicle_id: str, limit: int = 10):
    return db.query(models.Telemetry).filter(
        models.Telemetry.vehicleId == vehicle_id
    ).order_by(models.Telemetry.timestamp.desc()).limit(limit).all()
