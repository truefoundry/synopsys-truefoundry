import argparse
import logging

from servicefoundry import Build, PythonBuild, Resources, Service

logging.basicConfig(level=logging.INFO)

# parsing the input arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "--workspace_fqn",
    type=str,
    required=True,
    help="fqn of workspace where you want to deploy",
)
args = parser.parse_args()

# creating a service object and defining all the configurations
service_names = ["synopsys2-model-aug", "synopsys2-model-3-328mb", "synopsys-demo-model-08"]
model_names = ["model_aug_2022.h5", "model_3_328MB.h5", "demo_model_08.h5"]

# service_names = ["synopsys2-model-3-328mb"]
# model_names = ["model_3_328MB.h5"]

for model_name, service_name in zip(model_names, service_names):
    service = Service(
        name=service_name,
        image=Build(
            build_spec=PythonBuild(
                command="apt-get -y update && apt-get install -y libgl1 && uvicorn main:app --port 4000 --host 0.0.0.0",
                python_version="3.8.13",
            ),
        ),
        env={
            # These will automatically map the secret value to the environment variable.
            "MLF_HOST": "tfy-secret://user-truefoundry:synopsys-demo:MLF_HOST",
            "MLF_API_KEY": "tfy-secret://user-truefoundry:synopsys-demo:MLF_API_KEY",
            "MODEL_NAME": model_name,
            "RUN_ID_FOR_MODELS": "13e6bdffa50c458f8e9965a7130bbd09"
        },
        ports=[{"port": 4000}],
        resources=Resources(
            cpu_request=2, cpu_limit=3, memory_limit=4000, memory_request=2500
        ),
    )
    service.deploy(workspace_fqn=args.workspace_fqn)
