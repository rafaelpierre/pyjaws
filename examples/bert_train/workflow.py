from pyjaws.api.base import Cluster, Runtime, Workflow
from pyjaws.api.tasks import SparkPythonTask, Source
from databricks.sdk import WorkspaceClient
import os
from examples.bert_train.src import train

# Upload module into DBFS

w = WorkspaceClient()
python_script_path = "dbfs:/bert_train/src/train.py"

w.dbutils.fs.rm(python_script_path)

w.dbutils.fs.cp(
    from_ = f"file://{os.path.abspath(train.__file__)}",
    to = python_script_path
)

cluster = Cluster(
    job_cluster_key="ai_cluster",
    spark_version=Runtime.DBR_13_ML,
    num_workers=2,
    node_type_id="r3.xlarge",
    cluster_log_conf={"dbfs": {"destination": "dbfs:/home/cluster_log"}},
)

# Create a Task object.

train_task = SparkPythonTask(
    key="train",
    cluster=cluster,
    python_file=python_script_path,
    source = Source.WORKSPACE
)

# Create a Workflow object to define dependencies
# between previously defined tasks.

workflow = Workflow(name="distilbert_workflow", tasks=[train_task])
