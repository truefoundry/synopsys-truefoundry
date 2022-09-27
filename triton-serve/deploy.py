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
    ports=[{"port": 8000}], # Add {"port": 8001} to expose the gRPC port  
    resources=Resources(memory_request=2000, memory_limit=2500, cpu_request=3, cpu_limit='3500m'),
)

service.deploy(workspace_fqn=args.workspace_fqn)
