# PyJaws: A Pythonic Way to Define Databricks Jobs and Workflows

<p align="center">
        <img src="https://raw.githubusercontent.com/rafaelpierre/pyjaws/main/img/pyjaws.png" class="align-center" />
    </a>
</p>

<hr />

[![pypi](https://img.shields.io/badge/pypi-0.1.1-brightgreen?style=for-the-badge)](https://pypi.org/project/pyjaws/) ![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge) ![ruff](https://img.shields.io/badge/lint-ruff-gold?style=for-the-badge) ![cov](https://raw.githubusercontent.com/rafaelpierre/pyjaws/main/img/coverage.svg) ![databricks](https://img.shields.io/badge/Databricks-FF3621.svg?style=for-the-badge&logo=Databricks&logoColor=white) ![Jinja](https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black)

<hr />

* **PyJaws** enables declaring [Databricks Jobs and Workflows](https://docs.databricks.com/workflows/index.html) as Python code, allowing for:
  * Code Linting
  * Formatting
  * Parameter Validation
  * Modularity and reusability
* In addition to those, **PyJaws** also provides some nice features such as [cycle detection](https://networkx.org/documentation/stable/reference/algorithms/cycles.html) out of the box.

Folks who have used Python-based orchestration tools such as [Apache Airflow](https://airflow.apache.org/), [Luigi](https://luigi.readthedocs.io/en/stable/) and [Mage](https://pypi.org/project/mage-ai/) will be familiar with the concepts and the API if **PyJaws**.

* **PyJaws** leverages some existing libraries in order to allow for **modularisation**, **reusability** and **validation**, such as:
  * [Click](https://click.palletsprojects.com/en/8.1.x/) - for providing a rich CLI functionality
  * [Pydantic](https://docs.pydantic.dev/latest/) - for efficient parameter validation
  * [NetworkX](https://networkx.org/) - for Graph and Cycle Detection features
  * [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) - for templating

## Documentation

* Work in progress. Stay tuned!

## Development & Testing

* **PyJaws** can be tested locally for development purposes. To run unit tests, make sure `tox`, `pytest`, `pytest-cov`, and `coverage` are installed and from a bash terminal, simply run `tox`.

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

### Sample Results

Running `pyjaws create examples/simple_workflow` will result in the following Workflow being deployed to Databricks:

![workflow](https://github.com/rafaelpierre/pyjaws/blob/main/img/workflow.png?raw=true "Workflow")

By default, **pyjaws** also includes some useful tags into the workflows indicating which Git Repo hosts the Python definition, commit hash and when the workflow was last updated. For example:

![workflow](https://github.com/rafaelpierre/pyjaws/blob/main/img/tags.png?raw=true "Workflow")

## Disclaimer

* **PyJaws** is not developed, endorsed not supported by Databricks. It is provided as-is; no warranty is derived from using this package. For more details, please refer to the [license](https://github.com/rafaelpierre/pyjaws/blob/main/LICENSE.md).

## Reporting Bugs and Contributing

Feel free to create an issue if you feel something is not right. Contribution guidelines can be found [here](https://githubcom/rafaelpierre/pyjaws/blob/main/CONTRIBUTING.md).
