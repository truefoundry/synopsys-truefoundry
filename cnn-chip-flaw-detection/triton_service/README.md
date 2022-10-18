# Deploying models in a Triton `Service`

Notes
---

- The image size can be reduced if we can rewrite the whole preprocessing without using tensorflow
- The models can be easily hosted on s3 or any cloud bucket to reduce docker image size further
- Model can be exposed and used with grpc on port 8001


Keras to Saved Model
---

First we download the models and convert them to Tensorflow Saved Model


```shell
cd scripts
./run.sh
```

Setup
---

Next we install deployments SDK and login

```shell
pip install -U "servicefoundry<0.3.0"
sfy login
```

Deploy
---

Next we push our code and start a deployment

> Note: Replace the value of `--workspace_fqn` with the workspace you want from https://app.truefoundry.com/workspaces

```shell
python deploy.py --workspace_fqn "tfy-cluster-euwe1:demo-synopsys"
```


Curl Test (V2 Protocol)
---

```shell
cd client/
BASE_URL="https://synopsys-triton-serve-demo-synopsys-8000.tfy-ctl-euwe1-production.production.truefoundry.com"
curl -X POST -H 'Content-Type: application/json' -d @./input-v2-128.json "${BASE_URL}/v2/models/m2_new_128x128_74MB/infer"
curl -X POST -H 'Content-Type: application/json' -d @./input-v2-256.json "${BASE_URL}/v2/models/m1_initial_256x256_102MB/infer"
curl -X POST -H 'Content-Type: application/json' -d @./input-v2-256.json "${BASE_URL}/v2/models/m3_big_256x256_328MB/infer"
```


Output would look something like:

```json
{
  "id": "1",
  "model_name": "m3_big_256x256_328MB",
  "model_version": "1",
  "parameters": {
    "sequence_id": 0,
    "sequence_start": false,
    "sequence_end": false
  },
  "outputs": [
    {
      "name": "OUTPUT",
      "datatype": "FP32",
      "shape": [
        1,
        2
      ],
      "data": [
        0.6037940382957458,
        0.39620596170425415
      ]
    }
  ]
}
```


File Tree
---

```
.
├── .dockerignore
├── .gitignore
├── .sfyignore -> .dockerignore
├── Dockerfile
├── README.md
├── client
│   ├── client.py
│   ├── input-128.json
│   ├── input-256.json
│   ├── input-v2-128.json
│   ├── input-v2-256.json
│   └── requirements.txt
├── deploy.py
├── models
│   ├── m1_initial_256x256_102MB
│   │   ├── 1
│   │   │   └── .gitkeep
│   │   └── config.pbtxt
│   ├── m2_new_128x128_74MB
│   │   ├── 1
│   │   │   └── .gitkeep
│   │   └── config.pbtxt
│   ├── m3_big_256x256_328MB
│   │   ├── 1
│   │   │   └── .gitkeep
│   │   └── config.pbtxt
│   ├── model_m1_initial_256x256_102MB
│   │   ├── 1
│   │   │   └── model.savedmodel
│   │   │       ├── assets
│   │   │       ├── keras_metadata.pb
│   │   │       ├── saved_model.pb
│   │   │       └── variables
│   │   │           ├── variables.data-00000-of-00001
│   │   │           └── variables.index
│   │   └── config.pbtxt
│   ├── model_m2_new_128x128_74MB
│   │   ├── 1
│   │   │   └── model.savedmodel
│   │   │       ├── assets
│   │   │       ├── keras_metadata.pb
│   │   │       ├── saved_model.pb
│   │   │       └── variables
│   │   │           ├── variables.data-00000-of-00001
│   │   │           └── variables.index
│   │   └── config.pbtxt
│   ├── model_m3_big_256x256_328MB
│   │   ├── 1
│   │   │   └── model.savedmodel
│   │   │       ├── assets
│   │   │       ├── keras_metadata.pb
│   │   │       ├── saved_model.pb
│   │   │       └── variables
│   │   │           ├── variables.data-00000-of-00001
│   │   │           └── variables.index
│   │   └── config.pbtxt
│   └── preprocess
│       ├── 1
│       │   └── model.py
│       └── config.pbtxt
├── requirements.txt
└── scripts
    ├── convert_keras_to_savedmodel.py
    ├── requirements.txt
    └── run.sh
```


Python Client Test
---

```shell
cd client
pip install -r requirements.txt
HOST=synopsys-triton-serve-demo-synopsys-8000.tfy-ctl-euwe1-production.production.truefoundry.com
python client.py --ssl --host "${HOST}" --model_name "m2_new_128x128_74MB"  --data @./input-128.json
python client.py --ssl --host "${HOST}" --model_name "m1_initial_256x256_102MB"  --data @./input-256.json
python client.py --ssl --host "${HOST}" --model_name "m3_big_256x256_328MB"  --data @./input-256.json
```
