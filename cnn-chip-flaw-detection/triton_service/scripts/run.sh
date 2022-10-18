#!/bin/bash
set -ex

echo 'Checking environment ...'
pip install -r requirements.txt
echo 'Downloading ...'
curl https://tfy-dev-model-server-research-2022-10-16.s3.eu-west-1.amazonaws.com/synopsys/models/m1_initial_256x256_102MB.h5 -o m1_initial_256x256_102MB.h5
curl https://tfy-dev-model-server-research-2022-10-16.s3.eu-west-1.amazonaws.com/synopsys/models/m2_new_128x128_74MB.h5 -o m2_new_128x128_74MB.h5
curl https://tfy-dev-model-server-research-2022-10-16.s3.eu-west-1.amazonaws.com/synopsys/models/m3_big_256x256_328MB.h5 -o m3_big_256x256_328MB.h5
echo 'Converting ...'
python convert_keras_to_savedmodel.py --inp m1_initial_256x256_102MB.h5 --out ../models/model_m1_initial_256x256_102MB/1/model.savedmodel
python convert_keras_to_savedmodel.py --inp m2_new_128x128_74MB.h5 --out ../models/model_m2_new_128x128_74MB/1/model.savedmodel
python convert_keras_to_savedmodel.py --inp m3_big_256x256_328MB.h5 --out ../models/model_m3_big_256x256_328MB/1/model.savedmodel
echo 'Cleaning up ...'
rm *.h5
echo 'Done'
