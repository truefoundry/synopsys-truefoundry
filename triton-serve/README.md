Keras to Saved Model

```shell
cd scripts
pip install -r requirements.txt
python convert_keras_to_savedmodel.py --inp ../../model_3_328MB.h5 --out ../models/model_3_328mb/1/model.savedmodel
```


```
.
├── .dockerignore
├── .gitignore
├── .sfyignore -> .dockerignore
├── Dockerfile
├── README.md
├── client
│   ├── client.py
│   └── requirements.txt
├── models
│   ├── ensemble
│   │   ├── 1
│   │   │   └── .gitkeep
│   │   └── config.pbtxt
│   ├── model_3_328mb
│   │   └── 1
│   │       └── model.savedmodel
│   │           ├── assets
│   │           ├── keras_metadata.pb
│   │           ├── saved_model.pb
│   │           └── variables
│   │               ├── variables.data-00000-of-00001
│   │               └── variables.index
│   └── preprocess
│       ├── 1
│       │   └── model.py
│       └── config.pbtxt
├── requirements.txt
└── scripts
    ├── convert_keras_to_savedmodel.py
    └── requirements.txt
```
