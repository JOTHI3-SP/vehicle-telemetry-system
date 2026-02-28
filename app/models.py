from sqlalchemy import Column, Integer, Float, String, DateTime, Index
from datetime import datetime
from .database import Base

class Telemetry(Base):
    __tablename__ = "telemetry"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicleId = Column(String, nullable=False)
    speed = Column(Float, nullable=False)
    engineTemperature = Column(Float, nullable=False)
    batteryLevel = Column(Float, nullable=False)
    energyConsumption = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String, nullable=False)
    
    __table_args__ = (
        Index('idx_vehicle_timestamp', 'vehicleId', timestamp.desc()),
    )
