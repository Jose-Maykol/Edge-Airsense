from fastapi import FastAPI
import app.firestore_config
from app.routers import broker_service, device_service
from app.routers.tasks import automated_task_service
from app.routers.tasks.automated_task_service import scheduler

app = FastAPI()
app.include_router(broker_service.router)
app.include_router(device_service.router)
app.include_router(automated_task_service.router)

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
