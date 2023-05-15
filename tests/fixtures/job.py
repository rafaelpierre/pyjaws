from pyjaws.api.base import Cluster, Runtime, Workflow
from pyjaws.api.tasks import (
    PythonWheelTask,
    NotebookTask,
    SparkPythonTask,
    Source,
)

import pytest


@pytest.fixture
def workflow_fixture() -> Workflow:
    cluster = Cluster(
        job_cluster_key="mycluster",
        spark_version=Runtime.DBR_13_ML,
        node_type_id="Standard_E4ds_v4",
        num_workers=3,
    )

    ingest_task = PythonWheelTask(
        key="ingest",
        cluster=cluster,
        entrypoint="iot",
        package_name="deepspeed",
        task_name="ingest",
        parameters=[
            f"dummy.parquet",
            "--output-db",
            "sensors",
            "--output-table",
            "bronze",
            "--zorder-column",
            "TagName",
            "--write-mode",
            "append",
        ],
    )

    aggregate_task = PythonWheelTask(
        key="aggregate",
        cluster=cluster,
        entrypoint="iot",
        libraries=[{"pypi": "deepspeed"}],
        package_name="deepspeed",
        task_name="aggregate",
        dependencies=[ingest_task],
        parameters=[
            "--input-db",
            "sensors",
            "--input-table",
            "bronze",
            "--output-db",
            "sensors",
            "--output-table",
            "silver",
            "--zorder-column",
            "TagName",
        ],
    )

    visualizations_notebook = NotebookTask(
        key="visualizations",
        cluster=cluster,
        dependencies=[aggregate_task],
        libraries=[{"pypi": "plotly"}],
        notebook_path="/Workspace/Shared/visualizations",
        source=Source.WORKSPACE,
    )

    cleanup_task = SparkPythonTask(
        key="cleanup",
        cluster=cluster,
        dependencies=[visualizations_notebook],
        python_file="/Workspace/Repos/bob@mail.com/utils/cleanup.py",
        source=Source.WORKSPACE,
    )

    workflow = Workflow(
        name="test_workflow_iot",
        tasks=[ingest_task, aggregate_task, visualizations_notebook, cleanup_task],
        tags={"test": "value"},
    )

    return workflow


@pytest.fixture
def workflow_fixture_no_tags() -> Workflow:
    cluster = Cluster(
        job_cluster_key="mycluster",
        spark_version=Runtime.DBR_13_ML,
        node_type_id="Standard_E4ds_v4",
        num_workers=3,
    )

    aggregate_task = PythonWheelTask(
        key="aggregate",
        cluster=cluster,
        entrypoint="iot",
        package_name="deepspeed",
        libraries=[{"pypi": "deepspeed"}],
        task_name="aggregate",
        parameters=[
            "--input-db",
            "sensors",
            "--input-table",
            "bronze",
            "--output-db",
            "sensors",
            "--output-table",
            "silver",
            "--zorder-column",
            "TagName",
        ],
    )

    workflow = Workflow(name="test_workflow_iot", tasks=[aggregate_task])

    return workflow
