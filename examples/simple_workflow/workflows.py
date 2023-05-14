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
    package_name = "my_package",
    entrypoint = "ingest",
    task_name = "ingest",
    libraries = [
        {
            "pypi": {
                "package": "deepspeed"
            }
        }
    ],
    parameters = [
        "my_parameter_value",
        "--output-table", "my_table"
    ]
)

transform_task = Task(
    key = "transform",
    cluster = cluster,
    package_name = "deepspeed",
    entrypoint = "deepspeed",
    task_name = "ingest",
    dependencies = [ingest_task],
    libraries = [{"pypi": "deepspeed"}],
    parameters = [
       "--num_nodes", "2",
       "--num_gpus", "2",
       "run_glue_classifier_bert_base.py"
    ]
)


# Create a Workflow object to define dependencies
# between previously defined tasks.

workflow = Workflow(
    name = "my_workflow",
    tasks = [ingest_task, transform_task]
)