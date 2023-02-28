import binascii

import cv2
import numpy
from cv2 import dnn_superres

# TODO serializer pickle
# TODO redis autoclean

def upscale(input_bytes: bytes, model_path: str) -> str:
    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel("edsr", 2)
    input_bytes = binascii.a2b_base64(input_bytes)
    image_array = numpy.asarray(bytearray(input_bytes), dtype='uint8')
    image_decode = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    result = scaler.upsample(image_decode)
    image_encode = cv2.imencode('.png', result)
    encoded_array = numpy.array(image_encode[1])
    byte_encode = encoded_array.tobytes()
    byte_encode = binascii.b2a_base64(byte_encode).decode('utf-8')
    return byte_encode
