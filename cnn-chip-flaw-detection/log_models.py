import os
import pathlib
from typing import List

import mlfoundry

# Here we are uploading the model files as artifacts to a run
# These models can be dowloaded by running `run.sh` in the same directory
MODEL_FILES = ["m1_initial_256x256_102MB.h5", "m2_new_128x128_74MB.h5", "m3_big_256x256_328MB.h5"]

mlfoundry.login()
client = mlfoundry.get_client()
run = client.create_run(project_name="synopsys-cnn-chip-flaw-detect", run_name="pretrained-cnn-models")

for model_path in MODEL_FILES:
    model_name, *_ = os.path.splitext(os.path.basename(model_path))
    run.log_artifact(local_path=model_path, artifact_path=model_name)
