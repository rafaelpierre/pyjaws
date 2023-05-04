# 🦈 pyjaws

* **pyjaws** is a Python Framework which provides a pythonic way to define Databricks Jobs and Workflows.
* It leverages some existing libraries in order to allow for modularisation, reusability and validation, such as:
    * Click - for providing CLI functionality
    * Pydantic - for parameter validation
    * NetworkX - for Graph and Cycle Detection features
    * Jinja2 - for templating

## Getting Started

* First step is installing `pyjaws`:

```bash
pip install https://github.com/rafaelpierre/pyjaws
```

* Once it's installed, define your Databricks Workspace authentication variables:

```bash
export DATABRICKS_HOST = ...
export DATABRICKS_TOKEN = ...
```

* Last, define your Workflow Tasks (see `examples`) and run:

```bash
pyjaws create path/to/your/workflow_definitions
```

### Example

```python
from pyjaws.api.base import (
    Cluster,
    Runtime,
    Task,
    Workflow
)

cluster = Cluster(
    job_cluster_key = "ai_cluster",
    spark_version = Runtime.DBR_13_ML,
    num_workers = 2,
    node_type_id = "Standard_DS3_v2",
    cluster_log_conf = {
        "dbfs": {
            "destination": "dbfs:/home/cluster_log"
        }
    }
)


# Create a Task object.

ingest_task = Task(
    key = "ingest",
    cluster = cluster,
    entrypoint = "iot",
    task_name = "ingest",
    parameters = [
        f"my_parameter_value",
        "--output-table", "my_table"
    ]
)

transform_task = Task(
    key = "transform",
    cluster = cluster,
    entrypoint = "iot",
    task_name = "ingest",
    dependencies = [ingest_task],
    parameters = [
        f"my_parameter_value2",
        "--input-table", "my_table"
        "--output-table", "output_table"
    ]
)


# Create a Workflow object to define dependencies
# between previously defined tasks.

workflow = Workflow(
    name = "my_workflow",
    tasks = [ingest_task, transform_task]
)
```

### Sample Results

Running `pyjaws create examples/simple_workflow` will result in the following Workflow being deployed to Databricks:

<img src="https://github.com/rafaelpierre/pyjaws/blob/main/img/workflow.png?raw=true />

By default, **pyjaws** also includes some useful tags into the workflows indicating which Git Repo hosts the Python definition, commit hash and when the workflow was last updated. For example:

<img src="https://github.com/rafaelpierre/pyjaws/blob/main/img/tags.png?raw=true />
