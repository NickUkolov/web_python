import binascii
import time
import redis
import cv2
import numpy
from celery import Celery
from flask import Flask, request, jsonify, Response, redirect, url_for, send_file

from upscale import upscale
from celery_app import celery_app, upscale_image, get_task

app = Flask(__name__)

celery_app.conf.update(app.config)
class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = ContextTask


@app.route('/upscale', methods=['POST'])
def upload_n_upscale():
    image = request.files.get('image')
    image_bytes = binascii.b2a_base64(image.read()).decode('utf-8')
    task = upscale_image.delay(image_bytes, upscale_model='EDSR_x2.pb')

    return jsonify({'task_id': task.id})
    # a = upscale(image_bytes, 'app/EDSR_x2.pb')
    # return Response(a)

@app.route('/processed/<string:task_id>', methods=['GET'])
def processed(task_id):
    task = get_task(task_id)
    result = binascii.a2b_base64(task.result)
    return Response(result, content_type='image/png')



if __name__ == '__main__':
    app.run()
