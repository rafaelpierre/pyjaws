from pyjaws.api.base import Cluster, Runtime, Workflow
from pyjaws.api.tasks import SparkPythonTask, Source
from databricks.sdk import WorkspaceClient
import os
from examples.bert_train.src import train

# Upload module into DBFS

cluster = Cluster(
    job_cluster_key="ai_cluster",
    spark_version=Runtime.DBR_13_ML_GPU,
    num_workers=2,
    node_type_id="g5.2xlarge",
    cluster_log_conf={"dbfs": {"destination": "dbfs:/home/cluster_log"}},
)

# Create a Task object.

train_task = SparkPythonTask(
    key="train",
    cluster=cluster,
    local_module=train,
    source = Source.WORKSPACE,
    libraries = [
        {"pypi": {
            "package": "torch==2.0.1"
        }}
    ]
)

# Create a Workflow object to define dependencies
# between previously defined tasks.

workflow = Workflow(name="distilbert_workflow", tasks=[train_task])
