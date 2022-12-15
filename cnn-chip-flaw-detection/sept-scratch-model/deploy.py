import argparse
import logging
from servicefoundry import ModelDeployment, TruefoundryModelRegistry, Resources

logging.basicConfig(level=logging.INFO, format=logging.BASIC_FORMAT)

parser = argparse.ArgumentParser()
parser.add_argument("--model_version_fqn", type=str, required=True, help="Model version FQN of the model from Truefoundry's Registry")
parser.add_argument("--workspace_fqn", type=str, required=True, help="Workspace to deploy to")
args, _ = parser.parse_known_args()


model_deployment = ModelDeployment(
    name="sept-scratch-model",
    model_source=TruefoundryModelRegistry(
        model_version_fqn=args.model_version_fqn
    ),
    resources=Resources(
        cpu_request=1, 
        cpu_limit=4, 
        memory_request=500, 
        memory_limit=1000,
        instance_family=["c6i"]
    )
)
deployment = model_deployment.deploy(workspace_fqn=args.workspace_fqn, wait=True)
