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

---
