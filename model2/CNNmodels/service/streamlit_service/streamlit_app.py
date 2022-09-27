import io
import os
import logging

import requests
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)
CLASSES = ["No Defect", "Defect Detected"]


def load_image():
    uploaded_file = st.file_uploader(label='Pick an image to test')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        im = Image.open(io.BytesIO(image_data))
        plt.imshow(np.array(im))
        plt.savefig('a.png')
        im2 = Image.open('a.png')
        st.image(im2)
        os.remove('a.png')
        return np.array(im)
    else:
        return None
    
    
def predict_fastapi(model_name, image):
    try:
        url = urljoin(os.getenv(f"FASTAPI_MODEL_{model_name}"), "/predict")
        response = requests.post(url=url, json=[image.tolist()])
        response = response.json()
        predicted_class = response["predicted_classes"][0]
        prediction = CLASSES[predicted_class]
        inference_time = response.elapsed.total_seconds()
    except Exception:
        logging.exception(f"Error while calling {url}")
        prediction = "ERROR"
        inference_time = -1.0
        
    return {
        "prediction": prediction,
        "prediction_time": inference_time, 
    }

def predict_triton(model_name, image):
    try:
        triton_base_url = os.getenv("TRITON_ENDPOINT")
        model_mapping = {
            "M1": ("m1_initial_256x256_102MB", (256, 256)),
            "M2": ("m2_new_128x128_74MB", (128, 128)),
            "M3": ("m3_big_256x256_328MB", (256, 256)),
        }
        model_name, shape = model_mapping[model_name]
        url = urljoin(triton_base_url, f"v2/models/{model_name}/infer")
        body = {
            "id": "1",
            "inputs": [
                {"name": "INPUT_IMAGE", "shape": [1, *image.shape], "datatype": "UINT8", "data": [image.tolist()]},
                {"name": "INPUT_RESIZE_SHAPE", "shape": [1, 2], "datatype": "INT32", "data": [shape]}
            ],
            "outputs": [{"name": "OUTPUT"}]
        }
        response = requests.post(url=url, json=body)
        predicted_class = np.argmax(response.json()["outputs"][0]["data"])
        prediction = CLASSES[predicted_class]
        inference_time = response.elapsed.total_seconds()
    except Exception:
        logging.exception(f"Error while calling {url}")
        prediction = "ERROR"
        inference_time = -1.0
        
    return {
        "prediction": prediction,
        "prediction_time": inference_time, 
    }
    


def main():
    st.title(f'Streamlit Demo for model: Synopsys')
    image = load_image()
    result = st.button('Run on image')
    if result:
        results_dict = {}
        st.write('Calculating results...')
        model_names = ["M1", "M2", "M3"]
        for model_name in model_names:
            results_dict[f"{model_name} (fastapi)"] = predict_fastapi(model_name, image)
            results_dict[f"{model_name} (triton, includes network time)"] = predict_triton(model_name, image)
        st.table(results_dict)


if __name__ == '__main__':
    main()
