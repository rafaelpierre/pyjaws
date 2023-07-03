# PyJaws: A Pythonic Way to Define Databricks JaWs (Jobs and Workflows)

<p align="center">
        <img src="https://raw.githubusercontent.com/rafaelpierre/pyjaws/main/img/pyjaws.png" class="align-center" />
    </a>
</p>

<hr />

[![pypi](https://img.shields.io/badge/pypi-0.1.5-brightgreen?style=for-the-badge)](https://pypi.org/project/pyjaws/) ![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge) ![ruff](https://img.shields.io/badge/lint-ruff-gold?style=for-the-badge) ![cov](https://raw.githubusercontent.com/rafaelpierre/pyjaws/main/img/coverage.svg) ![databricks](https://img.shields.io/badge/Databricks-FF3621.svg?style=for-the-badge&logo=Databricks&logoColor=white) ![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black) ![downloads](https://img.shields.io/pypi/dm/pyjaws?style=for-the-badge)

<hr />

* **PyJaws** enables declaring [Databricks Jobs and Workflows](https://docs.databricks.com/workflows/index.html) as Python code, allowing for:
  * Code Linting
  * Formatting
  * Parameter Validation
  * Modularity and reusability
* In addition to those, **PyJaws** also provides some nice features such as [cycle detection](https://networkx.org/documentation/stable/reference/algorithms/cycles.html) out of the box.

Folks who have used Python-based orchestration tools such as [Apache Airflow](https://airflow.apache.org/), [Luigi](https://luigi.readthedocs.io/en/stable/) and [Mage](https://pypi.org/project/mage-ai/) will be familiar with the concepts and the API if **PyJaws**.

## Getting Started

* First step is installing `pyjaws`:

```bash
pip install pyjaws
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

### Sample Job Definition

```python
from pyjaws.api.base import (
    Cluster,
    Runtime,
    Workflow
)
from pyjaws.api.tasks import PythonWheelTask

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

ingest_task = PythonWheelTask(
    key = "ingest",
    cluster = cluster,
    entrypoint = "iot",
    task_name = "ingest",
    parameters = [
        f"my_parameter_value",
        "--output-table", "my_table"
    ]
)

transform_task = PythonWheelTask(
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

### Extra Features

* **Context Manager** for **Cluster** declarations:

```python
# cluster created with context manager
with Cluster(
    job_cluster_key="mycluster_2",
    spark_version=Runtime.DBR_13_ML,
    node_type_id="Standard_E4ds_v4",
    num_workers=3,
) as cluster_2:
    task_2 = SparkPythonTask(
        key="task_2",
        cluster=cluster_2,
        python_file="/Workspace/Repos/bob@mail.com/utils/task_2.py",
        source=Source.WORKSPACE,
    )
```

* **Workflow preview/visualization** on notebooks:

```python
display(workflow)
```
Result:

![preview](https://github.com/rafaelpierre/pyjaws/blob/main/img/preview.png?raw=true "Preview")

## Deploying Jobs

If you have a folder containing multiple workflow definition files written in Python with **PyJaws**, it is quite simple to deploy all of them to your Databricks Workspace with a one liner:

`pyjaws create examples/simple_workflow`

This would result in the following Workflow being deployed to your workspace:

![workflow](https://github.com/rafaelpierre/pyjaws/blob/main/img/workflow.png?raw=true "Workflow")

By default, **pyjaws** also includes some useful tags into the workflows indicating which Git Repo hosts the Python definition, commit hash and when the workflow was last updated. For example:

![workflow](https://github.com/rafaelpierre/pyjaws/blob/main/img/tags.png?raw=true "Workflow")

## Documentation

* Work in progress. Stay tuned!

## Development & Testing

* **PyJaws** can be tested locally for development purposes. To run unit tests, make sure `tox`, `pytest`, `pytest-cov`, and `coverage` are installed and from a bash terminal, simply run `tox`.

## Disclaimer

* **PyJaws** is not developed, endorsed not supported by Databricks. It is provided as-is; no warranty is derived from using this package. For more details, please refer to the [license](https://github.com/rafaelpierre/pyjaws/blob/main/LICENSE.md).

## Reporting Bugs and Contributing

Feel free to create an issue if you feel something is not right. Contribution guidelines can be found [here](https://githubcom/rafaelpierre/pyjaws/blob/main/CONTRIBUTING.md).
