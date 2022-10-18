### A `Job` that trains a xgboost model

To run this example,

1. Git clone this repo

   ```shell
   git clone https://github.com/truefoundry/synopsys-truefoundry
   cd synopsys-truefoundry/xgboost-train
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
