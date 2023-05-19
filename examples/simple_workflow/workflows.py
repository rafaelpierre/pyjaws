from pyjaws.api.base import Cluster, Runtime, Task, Workflow
from pathlib import Path
import ruamel.yaml

CONFIG_FOLDER = Path("config")

cluster = Cluster(
    job_cluster_key="ai_cluster",
    spark_version=Runtime.DBR_13_ML,
    num_workers=2,
    node_type_id="Standard_DS3_v2",
    cluster_log_conf={"dbfs": {"destination": "dbfs:/home/cluster_log"}},
)

# Create a Task object.
ingest_task = Task(
    key="ingest",
    cluster=cluster,
    entrypoint="iot",
    task_name="ingest",
    parameters=[f"my_parameter_value", "--output-table", "my_table"],
)

transform_task = Task(
    key="transform",
    cluster=cluster,
    entrypoint="iot",
    task_name="ingest",
    dependencies=[ingest_task],
    parameters=[
        f"my_parameter_value2",
        "--input-table",
        "my_table" "--output-table",
        "output_table",
    ],
)

# Create a Workflow object to define dependencies
# between previously defined tasks.
workflow = Workflow(name="my_workflow", tasks=[ingest_task, transform_task])

if __name__ == "__main__":
    config_file = CONFIG_FOLDER / f"{workflow.name}.yml"

    with config_file.open("w") as f:
        f.write(ruamel.yaml.round_trip_dump(workflow.json(), indent=2))
