import json
from typing import Sequence

import cv2 as cv
import numpy as np
import tensorflow as tf
import triton_python_backend_utils as pb_utils


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

def prepare_images(
    images: Sequence[np.ndarray],
    threshold: int = 1,
    max_value: int = 1,
    target_width: int = 128,
    target_height: int = 128
):
    image_tensors = [
        prepare_image(
            image,
            threshold=threshold,
            max_value=max_value,
            target_width=target_width,
            target_height=target_height
        )
        for image in images
    ]
    return tf.stack(image_tensors).numpy()


class TritonPythonModel:
    def initialize(self, args):
        self.model_config = json.loads(args['model_config'])
        output0_config = pb_utils.get_output_config_by_name(self.model_config, "OUTPUT_0")
        self.output0_dtype = pb_utils.triton_string_to_numpy(output0_config['data_type'])

    def execute(self, requests):
        output0_dtype = self.output0_dtype
        responses = []
        for request in requests:
            # each request is a batch of images
            in_0 = pb_utils.get_input_tensor_by_name(request, "INPUT_0")
            image = prepare_images(
                in_0.as_numpy(),
                threshold=1,
                max_value=1,
                target_width=256,
                target_height=256
            )
            out_tensor_0 = pb_utils.Tensor("OUTPUT_0", image.astype(output0_dtype))
            inference_response = pb_utils.InferenceResponse(output_tensors=[out_tensor_0])
            responses.append(inference_response)
        return responses

    def finalize(self):
        print('Cleaning up...')