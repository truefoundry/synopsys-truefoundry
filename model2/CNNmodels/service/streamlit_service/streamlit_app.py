import io
import os
from PIL import Image
import streamlit as st
from predict import batch_predict, run as mlf_run
import matplotlib.pyplot as plt
import numpy as np


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
        resp = batch_predict([result], 0)
        results_dict['M1'] = {
            "prediction": "No Defect" if resp["predicted_classes"][0]==0 else "Defect Detected",
            "prediction_time": resp["average_inference_time"]
        }

        resp = batch_predict([result], 1)
        results_dict['M2'] = {
            "prediction": "No Defect" if resp["predicted_classes"][0]==0 else "Defect Detected",
            "prediction_time": resp["average_inference_time"]
        }

        resp = batch_predict([result], 2)
        results_dict['M3'] = {
            "prediction": "No Defect" if resp["predicted_classes"][0]==0 else "Defect Detected",
            "prediction_time": resp["average_inference_time"]
        }
        st.table(results_dict)
        

if __name__ == '__main__':
    main()
