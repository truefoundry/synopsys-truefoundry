import argparse
import logging

from servicefoundry import Build, Job, PythonBuild, Resources, Schedule

logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser()
parser.add_argument(
    "--workspace_fqn", type=str, required=True, help="fqn of the workspace to deploy to"
)
args = parser.parse_args()

# servicefoundry uses this specification to automatically create a Dockerfile and build an image,
python_build = PythonBuild(
    python_version="3.9",
    command="python test_model.py",
)
env = {
    # These will automatically map the secret value to the environment variable.
    "MLF_HOST": "tfy-secret://user-truefoundry:synopsys-demo:MLF_HOST",
    "MLF_API_KEY": "tfy-secret://user-truefoundry:synopsys-demo:MLF_API_KEY",
}
job = Job(
    name="synopsys-zgboost-train",
    image=Build(build_spec=python_build),
    env=env,
    resources=Resources(
        cpu_request=1, cpu_limit=1.5, memory_request=2000, memory_limit=2500
    ),
    trigger=Schedule(schedule="0 */12 * * *"),
)
job.deploy(workspace_fqn=args.workspace_fqn)