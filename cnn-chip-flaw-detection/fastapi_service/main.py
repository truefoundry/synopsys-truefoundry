import os
import glob
import pathlib
from datetime import datetime
from typing import List

import pandas as pd
import numpy as np
import cv2 as cv
import tensorflow as tf
from adabelief_tf import AdaBeliefOptimizer
from tensorflow_addons.losses import SigmoidFocalCrossEntropy
from tensorflow.python.ops.numpy_ops import np_config

from fastapi import FastAPI
import mlfoundry

np_config.enable_numpy_behavior()


def convert_image_to_binary_image(img: np.ndarray, threshold: int = 1, max_value: int = 1) -> np.ndarray:
    ret, bin_img = cv.threshold(img, thresh=threshold, maxval=max_value, type=cv.THRESH_BINARY)
    bin_img = bin_img.astype('float32')
    return bin_img


def transform_img_dimension(img: np.ndarray, target_width: int = 128, target_height: int = 128) -> np.ndarray:
    img = img.astype('uint8')
    bin_image = convert_image_to_binary_image(img)
    bin_3dimg = tf.expand_dims(input=bin_image, axis=2)
    bin_img_reshaped = tf.image.resize_with_pad(image=bin_3dimg, target_width=target_width, target_height=target_height, method="bilinear")
    xformed_img = np.squeeze(bin_img_reshaped, axis=2)
    # print(xformed_img.shape)
    return xformed_img.copy()


def transform_waferMap_dimension(input_img: np.ndarray, target_width: int = 128, target_height: int = 128) -> np.ndarray:
    img = input_img.copy()
    xformed_img = transform_img_dimension(img, target_width=target_width, target_height=target_height)
    del img
    return xformed_img


def load_model(model_filepath: pathlib.Path) -> tf.keras.models.Sequential:
    assert os.path.exists(model_filepath)
    model = tf.keras.models.load_model(
        model_filepath,
        custom_objects={
            "AdaBeliefOptimizer": AdaBeliefOptimizer,
            "SigmoidFocalCrossEntropy": SigmoidFocalCrossEntropy
        }
    )
    return model

def get_input_df(dataset_path: str):
    testDF = pd.concat([pd.read_pickle(fn) for fn in glob.glob(os.path.join(dataset_path, "wm811k_*_testing.pkl"))]).reset_index(drop=True)
    testDF.rename(columns={"waferMap": "WAFER_MAP"}, inplace=True)
    xformedTestDF: pd.DataFrame = testDF.copy(deep=True)
    xformedTestDF["WAFER_MAP"] = testDF.apply(transform_waferMap_dimension, key_name="WAFER_MAP", target_width=128, target_height=128, axis=1)
    # use 256x256 for the model with input 256x256 input dimension
    # xformedTestDF["waferMap"] = testDF.apply(transform_waferMap_dimension, key_name="WAFER_MAP", target_width=256, target_height=256, axis=1)
    xformedTestDF["SCRATCH_LABEL"] = (xformedTestDF.failureNum == 6).astype(int)
    return xformedTestDF

def predictScratchForWafer(imageArrayList: List[np.ndarray], model: tf.keras.models.Sequential) -> np.ndarray:
    try:
        # print(f"image shape: {imageArray.shape}")
        inp_arr = [imageArray.reshape(1, imageArray.shape[0], imageArray.shape[1], 1).astype('float') for imageArray in imageArrayList]
        inp_arr = tf.experimental.numpy.vstack(tuple(inp_arr))
        pred_list = model.predict_on_batch(inp_arr)
        # print(f"prediction: {pred}")
        return [np.squeeze(pred) for pred in pred_list]
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

# Now we fetch one of the models from the run created by `log_models.py` earlier
MODEL_NAME = os.getenv("MODEL_NAME")
run = mlfoundry.get_client().get_run_by_fqn(run_fqn=os.getenv("RUN_FQN"))
local_path = run.download_artifact(path=MODEL_NAME)
model_filepath = os.path.join(local_path, f"{MODEL_NAME}.h5")
model = load_model(model_filepath=model_filepath)
model.load_weights(model_filepath)

# Set the image width and height expected by the model
if '128x128' in MODEL_NAME:
    IMAGE_WIDTH = 128
    IMAGE_HEIGHT = 128
else:
    IMAGE_WIDTH = 256
    IMAGE_HEIGHT = 256


# next we wrap our predict function in a fastapi route
app = FastAPI(docs_url="/")

@app.post("/predict")
def batch_predict(input_array: List[List[List[float]]]):
    start_t = datetime.now()
    xformed_input_array = [
        transform_waferMap_dimension(np.array(img), IMAGE_WIDTH, IMAGE_HEIGHT) 
        for img in input_array
    ]
    outputs = predictScratchForWafer(xformed_input_array, model)
    pred = [int(output.argmax()) for output in outputs ]
    end_t = datetime.now()
    avg_time = (end_t-start_t)/(len(input_array))
    return {
        "average_inference_time": avg_time,
        "predicted_classes": pred
    }