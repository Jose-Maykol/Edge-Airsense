from fastapi import FastAPI
import app.firestore_config
from app.routers import user_devices_actions, devices
from app.routers.tasks import tasks

app = FastAPI()
app.include_router(user_devices_actions.router)
app.include_router(devices.router)
app.include_router(tasks.router)

# @app.on_event("shutdown")
# def shutdown_scheduler():
#     scheduler.shutdown()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
