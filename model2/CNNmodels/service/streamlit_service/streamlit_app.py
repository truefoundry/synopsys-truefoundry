import io
import os

import requests
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from urllib.parse import urljoin


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


def main():
    st.title(f'Streamlit Demo for model: Synopsys')
    image = load_image()
    result = st.button('Run on image')
    if result:
        results_dict = {}
        st.write('Calculating results...')

        st.write("Results without using Triton Server")
        model_names = ["M1", "M2", "M3"]

        for model_name in model_names:
            resp = requests.post(url=urljoin(os.getenv(f"FASTAPI_MODEL_{model_name}"), "/predict"), json=[image.tolist()]).json()
            results_dict[model_name] = {
                "prediction": "No Defect" if resp["predicted_classes"][0]==0 else "Defect Detected",
                "prediction_time": resp["average_inference_time"]
            }
        st.table(results_dict)


if __name__ == '__main__':
    main()
