from celery import Celery
from celery.result import AsyncResult

from upscale import upscale

celery_app = Celery(
    "celery_app",
    backend="redis://redis:6379/1",
    broker="redis://redis:6379/2",
)


def get_task(task_id: str) -> AsyncResult:
    return AsyncResult(task_id, app=celery_app)


@celery_app.task
def upscale_image(image_str: str, upscale_model: str) -> str:
    return upscale(image_str, upscale_model)
