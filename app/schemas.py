from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class TelemetryCreate(BaseModel):
    vehicleId: str
    speed: float = Field(ge=0)
    engineTemperature: float
    batteryLevel: float = Field(ge=0, le=100)
    energyConsumption: float
    latitude: float
    longitude: float
    timestamp: Optional[datetime] = None
    
    @field_validator('speed')
    @classmethod
    def validate_speed(cls, v):
        if v < 0:
            raise ValueError('speed must be >= 0')
        return v
    
    @field_validator('batteryLevel')
    @classmethod
    def validate_battery(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('batteryLevel must be between 0 and 100')
        return v

class TelemetryResponse(BaseModel):
    id: int
    vehicleId: str
    speed: float
    engineTemperature: float
    batteryLevel: float
    energyConsumption: float
    latitude: float
    longitude: float
    timestamp: datetime
    status: str
    
    class Config:
        from_attributes = True
