# synopsys-truefoundry
The following is directory structure for the repository:
```
├── README.md
├── Truefoundry-models.pptx
├── model1
│   ├── XGB.model
│   └── train_job
│       ├── deploy.py
│       ├── requirements.txt
│       └── test_model.py
├── model2
│   └── CNNmodels
│       ├── conda_env.yaml
│       ├── log_models.py
│       ├── service
│       │   ├── __init__.py
│       │   ├── deploy.py
│       │   ├── deploy_streamlit.py
│       │   ├── main.py
│       │   ├── requirements.txt
│       │   ├── streamlit_app.py
│       │   └── streamlit_requirements.txt
│       └── test_data
│           ├── wm811k_nonScratch_testing.pkl
│           ├── wm811k_noneDefect_testing.pkl
│           └── wm811k_scratch_testing.pkl
└── triton-serve
    ├── Dockerfile
    ├── README.md
    ├── client
    │   ├── client.py
    │   └── requirements.txt
    ├── models
    │   ├── ensemble
    │   │   ├── 1
    │   │   └── config.pbtxt
    │   ├── model_3_328mb
    │   │   ├── 1
    │   │   └── config.pbtxt
    │   └── preprocess
    │       ├── 1
    │       │   └── model.py
    │       └── config.pbtxt
    ├── requirements.txt
    └── scripts
        ├── convert_keras_to_savedmodel.py
        └── requirements.txt
```

###
Model 1:
```
python deploy.py --workspace_fqn <paste your workspace fqn from the dashboard here>

```

* For tracking the experimentation tracking dashboard -> https://app.develop.truefoundry.tech/mlfoundry
* Click on project `synopsys-xgb-model1` to view the log params/metrics

###
Model 2:
```
```