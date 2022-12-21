Job Trigger Example
---

Install release candidate version of servicefoundry

```
pip install -U "servicefoundry==0.6.3rc1"
```

To deploy and trigger

```
python deploy_and_trigger.py --workspace-fqn <YOUR-WORKSPACE-FQN>
```

-----

You can trigger a job using the Job's deployment fqn. It can be found on the Job Details page on the UI

### Python

1. With the pre-configured command

```python
from servicefoundry.internal.experimental import trigger_job

DEPLOYMENT_FQN = "<JOB-DEPLOYMENT-FQN>"  # E.g. tfy-cluster-euwe1:demo-tfy:train-iris-ex:1

result = trigger_job(deployment_fqn=deployment.fqn, command=[])

print("Trigger Job result:", result)
```

2. With a custom command

```python
from servicefoundry.internal.experimental import trigger_job

DEPLOYMENT_FQN = "<JOB-DEPLOYMENT-FQN>"  # E.g. tfy-cluster-euwe1:demo-tfy:train-iris-ex:1

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
```

### CLI

1. With the pre-configured command

```shell
SFY_EXPERIMENTAL=1 sfy trigger job --deployment_fqn <JOB-DEPLOYMENT-FQN>
```

2. With a custom command


```shell
SFY_EXPERIMENTAL=1 sfy trigger job --deployment_fqn <JOB-DEPLOYMENT-FQN> -- python main.py --test-size 0.33 --c 1.5 --n-jobs 4 --max-iter 200 --random-state 100
```