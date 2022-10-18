import argparse
import logging

from servicefoundry import Build, Job, PythonBuild, Resources, Schedule

logging.basicConfig(level=logging.INFO)

# We take in the workspace fqn from a user. Visit https://app.truefoundry.com/workspaces to get FQN
parser = argparse.ArgumentParser()
parser.add_argument(
    "--workspace_fqn", type=str, required=True, help="fqn of the workspace to deploy to"
)
args = parser.parse_args()

# We now define our Job, we provide it a name, which script to run, environment variables and resources
job = Job(
    name="synopsys-xgboost-train",
    image=Build(
        build_spec=PythonBuild(
            python_version="3.9",
            command="python train.py",
        )
    ),
    env={
        # These will automatically map the secret value to the environment variable.
        "MLF_HOST": "https://app.truefoundry.com/",
        "MLF_API_KEY": "tfy-secret://demo-synopsis:synopsys-demo:MLF_API_KEY",
    },
    env=env,
    resources=Resources(
        cpu_request=1, cpu_limit=1.5, memory_request=2000, memory_limit=2500
    ),
    trigger=Schedule(schedule="0 0 1 * *"),
)

# Finally, we call deploy to push it to Truefoundry platform
job.deploy(workspace_fqn=args.workspace_fqn)
