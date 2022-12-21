import argparse
import logging

from servicefoundry import Job, Build, PythonBuild, Resources
from servicefoundry.internal.experimental import trigger_job

logging.basicConfig(level=logging.INFO, format=logging.BASIC_FORMAT)
parser = argparse.ArgumentParser()
parser.add_argument("--workspace-fqn", type=str, required=True, help="Workspace to deploy to")
args = parser.parse_args()


job = Job(
    name='train-iris-ex',
    image=Build(
        build_spec=PythonBuild(
            python_version='3.9',
            requirements_path='requirements.txt',
            command="python main.py",
        )
    ),
    timeout=3600,
    resources=Resources(cpu_limit=0.5, memory_limit=500)
)
deployment = job.deploy(workspace_fqn=args.workspace_fqn)

print('=' * 10)
print(deployment.fqn)
print('=' * 10)

result = trigger_job(
    deployment_fqn=deployment.fqn,
    command=[
        "python main.py",
        "--test-size 0.33",
        "--c 1.5",
        "--n-jobs 4",
        "--max-iter 200",
        "--random-state 100"
    ]
)

print("Trigger Job result:", result)