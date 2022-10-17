import tensorflow as tf

import os
from typing import (List)
from adabelief_tf import AdaBeliefOptimizer
from tensorflow_addons.losses import SigmoidFocalCrossEntropy
import pathlib
import mlfoundry as mlf
# import matplotlib.pyplot as plt

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

MODEL_FILES = [ "model_aug_2022.h5", "model_3_328MB.h5", "demo_model_08.h5" ]
client = mlf.get_client()
run = client.create_run(project_name="synopsys-model2")

for model_path in MODEL_FILES:
    run.log_artifact(local_path=model_path, artifact_path=model_path[0:-3])
