import argparse
import logging

from servicefoundry import Build, PythonBuild, Resources, Service

logging.basicConfig(level=logging.INFO)

# We take in the workspace fqn from a user. Visit https://app.truefoundry.com/workspaces to get FQN
parser = argparse.ArgumentParser()
parser.add_argument(
    "--workspace_fqn", type=str, required=True, help="fqn of the workspace to deploy to"
)
args = parser.parse_args()

# We will create one service for each model we have
MODEL_NAME_TO_SERVICE_NAME =  {
    "m1_initial_256x256_102MB": "synopsys-model-m1", 
    "m2_new_128x128_74MB": "synopsys-model-m2",
    "m3_big_256x256_328MB":  "synopsys-model-m3",   
}


for model_name, service_name in MODEL_NAME_TO_SERVICE_NAME.items():
    # We now define our Service, we provide it a name, which script to run, environment variables and resources
    service = Service(
        name=service_name,
        image=Build(
            build_spec=PythonBuild(
                python_version="3.9",
                command="apt-get -y update && apt-get install -y libgl1 && uvicorn main:app --port 8000 --host 0.0.0.0",
            ),
        ),
        env={
            # These will automatically map the secret value to the environment variable.
            "MLF_HOST": "https://app.truefoundry.com/",
            "MLF_API_KEY": "tfy-secret://demo-synopsis:synopsys-demo:MLF_API_KEY",
            "MODEL_NAME": model_name,
            "RUN_FQN": "truefoundry/demo-synopsis/synopsys-cnn-chip-flaw-detect/pretrained-cnn-models"
        },
        ports=[{"port": 8000}],
        resources=Resources(
            cpu_request=2.5, cpu_limit=3, memory_request=1200, memory_limit=1500, 
        ),
    )
    # Finally, we call deploy to push it to Truefoundry platform
    service.deploy(workspace_fqn=args.workspace_fqn)
    print("=" * 100)
