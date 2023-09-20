from pyjaws.pyjaws.api.base import Cluster, Runtime, Workflow
from pyjaws.pyjaws.api.tasks import (
    BaseTask,
    PythonWheelTask,
    NotebookTask,
    SparkPythonTask,
    Source
)

from tests.fixtures.job import workflow_fixture

import pytest

# Test Cluster class
def test_cluster_init():
    cluster = Cluster(
        job_cluster_key="mycluster",
        spark_version=Runtime.DBR_13_ML,
        node_type_id="Standard_E4ds_v4",
        num_workers=3,
    )
    assert isinstance(cluster, Cluster)
    assert cluster.job_cluster_key == "mycluster"
    assert cluster.spark_version == Runtime.DBR_13_ML
    assert cluster.node_type_id == "Standard_E4ds_v4"
    assert cluster.num_workers == 3

# Test BaseTask class
def test_base_task_init():
    cluster = Cluster(
        job_cluster_key="mycluster",
        spark_version=Runtime.DBR_13_ML,
        node_type_id="Standard_E4ds_v4",
        num_workers=3,
    )
    base_task = BaseTask(key="task_key", cluster=cluster)
    assert isinstance(base_task, BaseTask)
    assert base_task.key == "task_key"
    assert base_task.cluster == cluster

# Test Workflow class
def test_workflow_init(workflow_fixture):
    assert workflow_fixture.name == "test_workflow_iot"
    # Add more assertions based on the actual structure of your workflow