Notes
---

- The image size can be reduced if we can rewrite the whole preprocessing without using tensorflow
- The models can be easily hosted on s3 or any cloud bucket to reduce docker image size further
- Model can be exposed andused with grpc on port 8001


Keras to Saved Model
---

```shell
cd scripts
./run.sh
```

Deploy
---

One time setup
```shell
sfy use server https://app.develop.truefoundry.tech/
sfy login
pip install -U servicefoundry==0.2.7
```

```shell
python deploy.py --workspace_fqn "v1:tfy-dev-cluster:synopsys-demo"
```


Curl Test (V2 Protocol)
---

```shell
cd client/
BASE_URL="https://synopsys-triton-serve-synopsys-demo-8000.tfy-ctl-euwe1-develop.develop.truefoundry.tech"
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
HOST=synopsys-triton-serve-synopsys-demo-8000.tfy-ctl-euwe1-develop.develop.truefoundry.tech
python client.py --ssl --host "${HOST}" --model_name "m2_new_128x128_74MB"  --data @./input-128.json
python client.py --ssl --host "${HOST}" --model_name "m1_initial_256x256_102MB"  --data @./input-256.json
python client.py --ssl --host "${HOST}" --model_name "m3_big_256x256_328MB"  --data @./input-256.json
```
