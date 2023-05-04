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