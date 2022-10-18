import argparse
import logging

from servicefoundry import Build, PythonBuild, Resources, Service

logging.basicConfig(level=logging.INFO)

# We take in the workspace fqn from a user. Visit https://app.truefoundry.com/workspaces to get FQN
parser = argparse.ArgumentParser()
parser.add_argument("--workspace_fqn", type=str, required=True, help="fqn of workspace where you want to deploy",)
args = parser.parse_args()

# creating a service object and defining all the configurations
service = Service(
    name="synopsys-streamlit-demo",
    image=Build(
        build_spec=PythonBuild(
            python_version="3.9",
            command="apt-get -y update && apt-get install -y libgl1 && streamlit run streamlit_app.py",
        ),
    ),
    env={
        "FASTAPI_MODEL_M1": "https://synopsys-model-m1-demo-synopsys.tfy-ctl-euwe1-production.production.truefoundry.com",
        "FASTAPI_MODEL_M2": "https://synopsys-model-m2-demo-synopsys.tfy-ctl-euwe1-production.production.truefoundry.com",
        "FASTAPI_MODEL_M3": "https://synopsys-model-m3-demo-synopsys.tfy-ctl-euwe1-production.production.truefoundry.com",
        "TRITON_ENDPOINT": "https://synopsys-triton-serve-demo-synopsys-8000.tfy-ctl-euwe1-production.production.truefoundry.com",
    },
    ports=[{"port": 8501}],
    resources=Resources(
        cpu_request=0.75, cpu_limit=1, memory_request=256, memory_limit=512, 
    ),
)
service.deploy(workspace_fqn=args.workspace_fqn)
