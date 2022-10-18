### Deploy a Streamlit app as a `Service`

In this example we will build a UI app on top of the deployed [fastapi](../fastapi_service/README.md) and [triton](../triton_service/README.md) services

> Note: This example assumes above fastapi and triton services are up and urls are configured in `[deploy.py](./deploy.py)`

To run this example,

1. Git clone this repo

   ```shell
   git clone https://github.com/truefoundry/synopsys-truefoundry
   cd synopsys-truefoundry/cnn-chip-flaw-detection/streamlit_service
   ```

1. Install servicefoundry

   ```shell
   pip install -U "servicefoundry<0.3.0"
   ```

1. Login to Truefoundry

   ```shell
   sfy login
   ```

1. Grab a workspace fqn from https://app.truefoundry.com/workspaces

1. Run `deploy.py` with the workspace fqn

   ```shell
   python deploy.py --workspace_fqn <your-workspace-fqn>
   ```

   E.g.

   ```shell
   python deploy.py --workspace_fqn "tfy-cluster-euwe1:demo-synopsys"
   ```