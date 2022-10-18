import argparse
import json
import uuid
from ssl import PROTOCOL_TLS_CLIENT, CERT_REQUIRED
from timeit import default_timer as timer

import numpy as np
from tritonclient.utils import np_to_triton_dtype
import tritonclient.http as httpclient

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='0.0.0.0:8000')
parser.add_argument('--ssl', action='store_true', default=False)
parser.add_argument('--model_name', type=str, choices=['m1_initial_256x256_102MB', 'm2_new_128x128_74MB', 'm3_big_256x256_328MB'], default='m2_new_128x128_74MB')
parser.add_argument('--data', type=str, required=True)
args = parser.parse_args()


if args.ssl:
    client_kwargs = {    
        "ssl": True,
    }
else:
    client_kwargs = {}
    

def _infer(client, input_image, resize_shape):
    input_image = input_image.astype(np.uint8)
    if len(input_image.shape) == 2:
        input_image = np.expand_dims(image, axis=0)
    if len(resize_shape.shape) == 1:
        resize_shape = np.expand_dims(resize_shape, axis=0)

    assert len(input_image.shape) == 3
    assert len(resize_shape.shape) == 2
    
    triton_input_image = httpclient.InferInput("INPUT_IMAGE", input_image.shape, np_to_triton_dtype(input_image.dtype)) 
    triton_input_image.set_data_from_numpy(input_image)
    
    triton_input_resize_shape = httpclient.InferInput("INPUT_RESIZE_SHAPE", resize_shape.shape, np_to_triton_dtype(resize_shape.dtype)) 
    triton_input_resize_shape.set_data_from_numpy(resize_shape)
    
    inputs = [triton_input_image, triton_input_resize_shape]
    triton_output_logits = httpclient.InferRequestedOutput("OUTPUT")
    outputs = [triton_output_logits]
    response = client.infer(args.model_name, inputs, request_id=str(uuid.uuid4()), outputs=outputs)
    result = response.get_response()
    logits = response.as_numpy("OUTPUT")
    return logits

def main():
    if "@" in args.data:
        with open(args.data[1:]) as f:
            data = json.load(f)
    else:
        data = json.loads(args.data)
    image = np.array(data["image"], dtype=np.uint8)
    resize_shape = np.array(data["resize_shape"], dtype=np.int32)
    with httpclient.InferenceServerClient(args.host, **client_kwargs) as client:
        start = timer()
        print(_infer(client, image, resize_shape))
        end = timer()
        print(f'\nFinished in {end - start} seconds')


if __name__ == '__main__':
    main()
