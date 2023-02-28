import binascii

from celery import Celery
from celery.result import AsyncResult

from upscale import upscale

celery_app = Celery('celery_app', backend='redis://localhost:6379/1', broker='redis://localhost:6379/2', )


def get_task(task_id):
    return AsyncResult(task_id, app=celery_app)


@celery_app.task
def upscale_image(image_bytes, upscale_model):
    return upscale(image_bytes, upscale_model)
