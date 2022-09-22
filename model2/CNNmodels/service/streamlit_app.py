import io
import os
from PIL import Image
import streamlit as st
from main import batch_predict
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
    st.title(f'Streamlit Demo for model: {os.getenv("MODEL_NAME")}')
    image = load_image()
    result = st.button('Run on image')
    if result:
        st.write('Calculating results...')
        resp = batch_predict([result])
        st.write(f'Prediction Class: {resp["predicted_classes"][0]}')


if __name__ == '__main__':
    main()