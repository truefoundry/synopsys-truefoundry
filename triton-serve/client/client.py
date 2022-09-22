import argparse
import ast
import uuid
from ssl import PROTOCOL_TLS_CLIENT, CERT_REQUIRED
from timeit import default_timer as timer

import numpy as np
from tritonclient.utils import np_to_triton_dtype
import tritonclient.http as httpclient

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='0.0.0.0:8000')
parser.add_argument('--ssl', action='store_true', default=False)
parser.add_argument('--model_name', type=str, default='ensemble')
parser.add_argument('--data', type=str, required=True)
args = parser.parse_args()

if args.ssl:
    class Urllib3SSLContextWrapper:
        def wrap_socket(self, sock, *_, **kwargs):
            from urllib3.util.ssl_ import ssl_wrap_socket
            return ssl_wrap_socket(sock, **kwargs)

    client_kwargs = {    
        "ssl": True,
        "ssl_context_factory": Urllib3SSLContextWrapper
    }
else:
    client_kwargs = {}
    

def _infer(client, input_image):
    input_image = input_image.astype(np.uint8)
    if len(input_image.shape) == 2:
        input_image = np.expand_dims(image, axis=0)
    assert len(input_image.shape) == 3
    triton_input_image = httpclient.InferInput("INPUT", input_image.shape, np_to_triton_dtype(input_image.dtype)) 
    triton_input_image.set_data_from_numpy(input_image)
    inputs = [triton_input_image]
    triton_output_logits = httpclient.InferRequestedOutput("OUTPUT")
    outputs = [triton_output_logits]
    response = client.infer(args.model_name, inputs, request_id=str(uuid.uuid4()), outputs=outputs)
    result = response.get_response()
    logits = response.as_numpy("OUTPUT")
    return logits

def main():
    image = np.array(ast.literal_eval(args.data))
    with httpclient.InferenceServerClient(args.host, **client_kwargs) as client:
        start = timer()
        print(_infer(client, image))
        end = timer()
        print(f'\nFinished in {end - start} seconds')


if __name__ == '__main__':
    main()