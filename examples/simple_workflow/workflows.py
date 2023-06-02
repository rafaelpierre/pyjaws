from pyjaws.api.base import Cluster, Runtime, Workflow
from pyjaws.api.tasks import PythonWheelTask

cluster = Cluster(
    job_cluster_key="ai_cluster",
    spark_version=Runtime.DBR_13_ML,
    num_workers=2,
    node_type_id="Standard_DS3_v2",
    cluster_log_conf={"dbfs": {"destination": "dbfs:/home/cluster_log"}},
)

# Create a Task object.

ingest_task = PythonWheelTask(
    key="test1",
    cluster=cluster,
    package_name="my_package",
    entrypoint="ingest",
    task_name="ingest",
    libraries=[{"pypi": {"package": "deepspeed"}}],
    parameters=["my_parameter_value", "--output-table", "my_table"],
)

transform_task = PythonWheelTask(
    key="transform",
    cluster=cluster,
    package_name="deepspeed",
    entrypoint="deepspeed",
    task_name="ingest",
    libraries=[{"pypi": "deepspeed"}],
    parameters=[
        "--num_nodes",
        "2",
        "--num_gpus",
        "2",
        "run_glue_classifier_bert_base.py",
    ],
)

# Task dependencies

ingest_task >> transform_task

# Create a Workflow object to define dependencies
# between previously defined tasks.

workflow = Workflow(name="my_workflow", tasks=[ingest_task, transform_task])
