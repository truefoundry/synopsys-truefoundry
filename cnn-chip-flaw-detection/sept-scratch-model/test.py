import logging
import argparse
import requests
from urllib.parse import urljoin

import cv2 as cv
import numpy as np
import tensorflow as tf
from PIL import Image

logging.basicConfig(level=logging.INFO, format=logging.BASIC_FORMAT)


def prepare_image(
    image: np.ndarray,
    threshold: int = 1,
    max_value: int = 1,
    target_width: int = 128,
    target_height: int = 128
):
    _, image = cv.threshold(image, thresh=threshold, maxval=max_value, type=cv.THRESH_BINARY)
    image = np.expand_dims(image, axis=2)
    image = tf.image.resize_with_pad(
        image,
        target_width=target_width,
        target_height=target_height,
        method="bilinear"
    )
    return image

parser = argparse.ArgumentParser()
parser.add_argument("--endpoint_url", type=str, required=True, help="Endpoint URL as shown on the Model Deployment Details Page")
parser.add_argument("--image", type=str, required=True, help="Image file path")
args, _ = parser.parse_known_args()

url = urljoin(args.endpoint_url, 'v1/models/sept-scratch-model:predict')
im = Image.open(args.image)
image_array = np.array(im)
image_array = prepare_image(image_array)
image_array = image_array.numpy()
print("Image shape": image_array.shape)
image_array = image_array.tolist()

response = requests.post(
    url,
    json={
        "instances": [
            {
                "conv2d_input": image_array.numpy().tolist()
            }
        ]
    }
)
print(response.status_code)
print(response.json())
