# synopsys-truefoundry

### Clone the repo

```shell
git clone https://github.com/truefoundry/synopsys-truefoundry
cd synopsys-truefoundry
```

### Install Python SDKs 

```
pip install -U -r requirements.txt
```

### Login to SDK

```shell
mlfoundry login 
```

### Model 1 - Xgboost Train Job

**See [guide](./xgboost-train/README.md) for detailed instructions**

```shell
cd xgboost-train
python deploy.py --workspace_fqn "tfy-cluster-euwe1:demo-synopsys"
```

* For tracking the experimentation tracking [dashboard](https://app.truefoundry.com/mlfoundry)
* Click on project `synopsys-xgb-classifier` to view the log params/metrics

### Model 2 - CNN Chip Flaw Detection

First we need to deploy the fastapi services.  
**See [guide](./cnn-chip-flaw-detection/fastapi_service/README.md) for detailed instructions**

```shell
cd cnn-chip-flaw-detection/fastapi_service
python deploy.py --workspace_fqn "tfy-cluster-euwe1:demo-synopsys"
```

Next we will deploy the triton server.  
**See [guide](./cnn-chip-flaw-detection/triton_service/README.md) for detailed instructions**

```shell
cd chip-flaw-detect-triton/triton_service
python deploy.py --workspace_fqn "tfy-cluster-euwe1:demo-synopsys"
```

Finally lets deploy the streamlit application:

Now simply run the command:

```shell
cd cnn-chip-flaw-detection/streamlit_service
python deploy.py --workspace_fqn "tfy-cluster-euwe1:demo-synopsys"
```

* You can find the endpoints on the applications page of [Truefoundry's dashboard](https://app.truefoundry.com/applications)

https://gist.github.com/shubham-rai-tf/9e088d9de6e14fca16a7908eb9c5071a
