# 🦈 pyjaws

![python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) ![black](https://shields.io/badge/formatting--black?logo=black&style=for-the-badge) ![ruff](https://img.shields.io/badge/Ruff-FCC21B.svg?style=for-the-badge&logo=Ruff&logoColor=yellow) ![databricks](https://img.shields.io/badge/Databricks-FF3621.svg?style=for-the-badge&logo=Databricks&logoColor=white)

* **PyJaws** is a Python Framework which provides a pythonic way to define Databricks Jobs and Workflows.
* It leverages some existing libraries in order to allow for modularisation, reusability and validation, such as:
    * [Click](https://click.palletsprojects.com/en/8.1.x/) - for providing CLI functionality
    * [Pydantic](https://docs.pydantic.dev/latest/) - for parameter validation
    * [NetworkX](https://networkx.org/) - for Graph and Cycle Detection features
    * [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) - for templating
 * Folks who have used Python-based orchestration tools such as [Apache Airflow](https://airflow.apache.org/), [Luigi](https://luigi.readthedocs.io/en/stable/) and [Mage](https://pypi.org/project/mage-ai/) will be familiar with the concepts and the API.

## Documentation

* Work in progress. Stay tuned!

## Testing

* **PyJaws** can be tested locally for development purposes. To run unit tests, make sure `tox`, `pytest`, `pytest-cov`, and `coverage` are installed and from a bash terminal, simply run `tox`.

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

![workflow](https://github.com/rafaelpierre/pyjaws/blob/main/img/workflow.png?raw=true "Workflow")

By default, **pyjaws** also includes some useful tags into the workflows indicating which Git Repo hosts the Python definition, commit hash and when the workflow was last updated. For example:

![workflow](https://github.com/rafaelpierre/pyjaws/blob/main/img/tags.png?raw=true "Workflow")
