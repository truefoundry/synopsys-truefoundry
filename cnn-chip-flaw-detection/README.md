Before we deploy the models as service,

1. First we will fetch the pretrained models

   ```shell
   ./run.sh
   ```

1. Next, we will log them with experiment tracking section as artifacts

   ```shell
   pip install -U "mlfoundry<0.5.0"
   python log_models.py
   ```

   > Note: This script will interactively ask you to provide an API Key from https://app.truefoundry.com/settings

   This would create a run with the logged artifacts (E.g. https://app.truefoundry.com/mlfoundry/373/run/b52108c3826f44649a3414268d9c8d89?tab=general-artifact )
---

**Next follow [fastapi service deployment guide](./fastapi_service/README.md) to deploy this models**