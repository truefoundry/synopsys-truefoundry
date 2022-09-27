# synopsys-truefoundry

The following is directory structure for the repository:
```
|-- README.md
|-- Truefoundry-models.pptx
|-- model1
|   |-- XGB.model
|   `-- train_job
|       |-- deploy.py
|       |-- requirements.txt
|       `-- test_model.py
|-- model2
|   |-- CNNmodels
|   |   |-- __init__.py
|   |   |-- conda_env.yaml
|   |   |-- log_models.py
|   |   |-- service
|   |   |   |-- __init__.py
|   |   |   |-- fastapi_service
|   |   |   |   |-- __init__.py
|   |   |   |   |-- deploy.py
|   |   |   |   |-- main.py
|   |   |   |   `-- requirements.txt
|   |   |   `-- streamlit_service
|   |   |       |-- __init__.py
|   |   |       |-- __pycache__
|   |   |       |-- deploy_streamlit.py
|   |   |       |-- streamlit_app.py
|   |   |       `-- streamlit_requirements.txt
|   |   `-- test_data
|   |       |-- wm811k_nonScratch_testing.pkl
|   |       |-- wm811k_noneDefect_testing.pkl
|   |       `-- wm811k_scratch_testing.pkl
|   `-- __init__.py
`-- triton-serve
    |-- Dockerfile
    |-- README.md
    |-- client
    |   |-- client.py
    |   |-- input-128.json
    |   |-- input-256.json
    |   |-- input-v2-128.json
    |   |-- input-v2-256.json
    |   `-- requirements.txt
    |-- deploy.py
    |-- models
    |   |-- m1_initial_256x256_102MB
    |   |   |-- 1
    |   |   `-- config.pbtxt
    |   |-- m2_new_128x128_74MB
    |   |   |-- 1
    |   |   `-- config.pbtxt
    |   |-- m3_big_256x256_328MB
    |   |   |-- 1
    |   |   `-- config.pbtxt
    |   |-- model_m1_initial_256x256_102MB
    |   |   `-- config.pbtxt
    |   |-- model_m2_new_128x128_74MB
    |   |   `-- config.pbtxt
    |   |-- model_m3_big_256x256_328MB
    |   |   `-- config.pbtxt
    |   `-- preprocess
    |       |-- 1
    |       |   `-- model.py
    |       `-- config.pbtxt
    |-- requirements.txt
    `-- scripts
        |-- convert_keras_to_savedmodel.py
        |-- requirements.txt
        `-- run.sh
```

### Model 1:
```
cd model1/train_job
python deploy.py --workspace_fqn v1:tfy-dev-cluster:synopsys-demo
```

* For tracking the experimentation tracking [dashboard](https://app.develop.truefoundry.tech/mlfoundry)
* Click on project `synopsys-xgb-classifier` to view the log params/metrics

### Model 2:

First we need to deploy the fastapi services.
```
cd model2/CNNmodels/service/fastapi_service
python deploy.py --workspace_fqn v1:tfy-dev-cluster:synopsys-demo
```

Next we will deploy the triton server:
```
cd triton-serve
python deploy.py --workspace_fqn v1:tfy-dev-cluster:synopsys-demo
```

Refer to [readme](./triton-serve/README.md) of triton serve for more information.

Finally lets deploy the streamlit application:

* Edit the [deploy_streamlit.py](./model2/CNNmodels/service/streamlit_service/deploy_streamlit.py) and add the fastapi and triton endpoints in the `env`.
* You can find the endpoints on the applications page of [truefoundry's dashboard](https://app.develop.truefoundry.tech/applications)

Now simply run the command:
```
cd model2/CNNmodels/service/streamlit_service
python deploy_streamlit.py --workspace_fqn v1:tfy-dev-cluster:synopsys-demo
```

