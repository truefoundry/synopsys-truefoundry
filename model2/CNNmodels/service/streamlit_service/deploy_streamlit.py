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


service = Service(
    name="synopsys-streamlit-demo",
    image=Build(
        build_spec=PythonBuild(
            command="apt-get -y update && apt-get install -y libgl1 && streamlit run streamlit_app.py",
            python_version="3.8.13",
            requirements_path="streamlit_requirements.txt"
        ),
    ),
    env={
        # These will automatically map the secret value to the environment variable.
        "MLF_HOST": "tfy-secret://user-truefoundry:synopsys-demo:MLF_HOST",
        "MLF_API_KEY": "tfy-secret://user-truefoundry:synopsys-demo:MLF_API_KEY",
        "RUN_ID_FOR_MODELS": "13e6bdffa50c458f8e9965a7130bbd09"
    },
    ports=[{"port": 8501}],
    resources=Resources(
        cpu_request=3.5, cpu_limit=4, memory_limit=4, memory_request=3
    ),
)
service.deploy(workspace_fqn=args.workspace_fqn)
