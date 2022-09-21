import tensorflow as tf
import cv2 as cv
import os
import glob
from typing import (List)
import mlfoundry as mlf
import pandas as pd
import numpy as np
from adabelief_tf import AdaBeliefOptimizer
from tensorflow_addons.losses import SigmoidFocalCrossEntropy
from datetime import datetime
from fastapi import FastAPI

import pathlib


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
        custom_objects={"AdaBeliefOptimizer": AdaBeliefOptimizer,
        "SigmoidFocalCrossEntropy": SigmoidFocalCrossEntropy}
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

def predictScratchForWafer(imageArray: np.ndarray, model: tf.keras.models.Sequential) -> np.ndarray:
    try:
        # print(f"image shape: {imageArray.shape}")
        pred = model.predict(imageArray.reshape(1, imageArray.shape[0], imageArray.shape[1], 1).astype('float'))
        # print(f"prediction: {pred}")
        return np.squeeze(pred)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

modelFileName = os.getenv("MODEL_NAME") #or "model_aug_2022.h5"
IMAGE_WIDTH=256
IMAGE_HEIGHT=256
if modelFileName=="model_aug_2022.h5":
    IMAGE_HEIGHT=128
    IMAGE_WIDTH=128

run_id = os.getenv("RUN_ID_FOR_MODELS") #or "13e6bdffa50c458f8e9965a7130bbd09"
modelFileName = f'{modelFileName[0:-3]}/{modelFileName}'

#client = mlf.get_client(tracking_uri="https://app.develop.truefoundry.tech", api_key="djE6dHJ1ZWZvdW5kcnk6dXNlci10cnVlZm91bmRyeTo0MTZjOTA=")
client = mlf.get_client()
run = client.get_run(run_id)
local_path=run.download_artifact(path=modelFileName, dest_path=".")

predictionModel = load_model(model_filepath=local_path)
predictionModel.load_weights(local_path)

app = FastAPI(docs_url="/")

@app.post("/predict")
def batch_predict(input_array: List[List[List[float]]]):
    start_t = datetime.now()
    xformed_input_array = [transform_waferMap_dimension(np.array(img), IMAGE_WIDTH, IMAGE_HEIGHT) for img in input_array]
    pred = [int(predictScratchForWafer(wm, predictionModel).argmax()) for wm in xformed_input_array ]
    end_t = datetime.now()
    avg_time = (end_t-start_t)/(len(input_array))
    return {
        "average_inference_time": avg_time,
        "predicted_classes": pred
    }

# import uvicorn
# if __name__=="__main__":
#     uvicorn.run(app, port=4000, log_level="info")
