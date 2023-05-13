from pyjaws.api.base import (
    Cluster,
    Task,
    Runtime,
    Workflow
)

import pytest


@pytest.fixture
def workflow_fixture() -> Workflow:

    cluster = Cluster(
        job_cluster_key = "mycluster",
        spark_version = Runtime.DBR_13_ML,
        node_type_id = "Standard_E4ds_v4",
        num_workers = 3
    )

    ingest_task = Task(
        key = "ingest",
        cluster = cluster,
        entrypoint = "iot",
        package_name = "deepspeed",
        task_name = "ingest",
        parameters = [
            f"dummy.parquet",
            "--output-db", "sensors",
            "--output-table", "bronze",
            "--zorder-column", "TagName",
            "--write-mode", "append"
        ]
    )

    aggregate_task = Task(
        key = "aggregate",
        cluster = cluster,
        entrypoint = "iot",
        libraries = [{"pypi": "deepspeed"}],
        package_name = "deepspeed",
        task_name = "aggregate",
        dependencies = [ingest_task],
        parameters = [
            "--input-db", "sensors",
            "--input-table", "bronze",
            "--output-db", "sensors",
            "--output-table", "silver",
            "--zorder-column", "TagName"
        ]
    )

    workflow = Workflow(
        name = "test_workflow_iot",
        tasks = [ingest_task, aggregate_task],
        tags = {
            "test": "value"
        }
    )

    return workflow


@pytest.fixture
def workflow_fixture_no_tags() -> Workflow:

    cluster = Cluster(
        job_cluster_key = "mycluster",
        spark_version = Runtime.DBR_13_ML,
        node_type_id = "Standard_E4ds_v4",
        num_workers = 3
    )

    aggregate_task = Task(
        key = "aggregate",
        cluster = cluster,
        entrypoint = "iot",
        package_name = "deepspeed",
        libraries = [{"pypi": "deepspeed"}],
        task_name = "aggregate",
        parameters = [
            "--input-db", "sensors",
            "--input-table", "bronze",
            "--output-db", "sensors",
            "--output-table", "silver",
            "--zorder-column", "TagName"
        ]
    )

    workflow = Workflow(
        name = "test_workflow_iot",
        tasks = [aggregate_task]
    )

    return workflow