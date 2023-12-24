from fastapi import APIRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..tasks.temperature_storage import temperature_storage_task
router = APIRouter()

# scheduler = AsyncIOScheduler()
# scheduler.add_job(temperature_storage_task, 'cron', hour='12,12,12', minute='32,33,34,35')
# scheduler.start()

