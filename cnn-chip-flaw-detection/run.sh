#!/bin/bash
set -ex

echo 'Downloading ...'
curl https://tfy-dev-model-server-research-2022-10-16.s3.eu-west-1.amazonaws.com/synopsys/models/m1_initial_256x256_102MB.h5 -o m1_initial_256x256_102MB.h5
curl https://tfy-dev-model-server-research-2022-10-16.s3.eu-west-1.amazonaws.com/synopsys/models/m2_new_128x128_74MB.h5 -o m2_new_128x128_74MB.h5
curl https://tfy-dev-model-server-research-2022-10-16.s3.eu-west-1.amazonaws.com/synopsys/models/m3_big_256x256_328MB.h5 -o m3_big_256x256_328MB.h5
