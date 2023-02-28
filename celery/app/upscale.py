import binascii

import cv2
import numpy
from cv2 import dnn_superres

# TODO serializer pickle
# TODO redis autoclean


def upscale(input_bytes: str, model_path: str) -> str:
    scaler = dnn_superres.DnnSuperResImpl_create()
    scaler.readModel(model_path)
    scaler.setModel("edsr", 2)

    input_str_to_bytes = binascii.a2b_base64(input_bytes)
    image_bytes_to_array = numpy.asarray(bytearray(input_str_to_bytes), dtype="uint8")
    image_decode = cv2.imdecode(image_bytes_to_array, cv2.IMREAD_COLOR)

    result = scaler.upsample(image_decode)

    image_encode = cv2.imencode(".png", result)
    encoded_array = numpy.array(image_encode[1])
    array_to_bytes = encoded_array.tobytes()
    bytes_to_str = binascii.b2a_base64(array_to_bytes).decode("utf-8")
    return bytes_to_str
