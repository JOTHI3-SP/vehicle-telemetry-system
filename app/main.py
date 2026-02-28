from fastapi import FastAPI
from .database import engine, Base
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Telemetry API", version="1.0.0")

app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}
