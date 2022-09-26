import argparse
import logging
from servicefoundry import Build, Service, DockerFileBuild, Resources

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--workspace_fqn", type=str, required=True, help="fqn of the workspace to deploy to")
args = parser.parse_args()

service = Service(
    name="synopsys-triton-serve",
    image=Build(build_spec=DockerFileBuild()),
    ports=[{"port": 8000}, {"port": 8001}],
    resources=Resources(memory_request=1200, memory_limit=1500, cpu_request=3, cpu_limit=4),
)

service.deploy(workspace_fqn=args.workspace_fqn)
