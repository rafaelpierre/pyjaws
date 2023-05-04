"""This module contains Databricks Jobs Workflows definitions for
the AI at Scale / IoT part of the PoC.
"""

from pyjaws.api.base import Task, Workflow
from examples.simple_workflow.compute.cluster import cluster
import os


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


# Create a Workflow object to define dependencies
# between previously defined tasks.

workflow = Workflow(
    name = "my_workflow",
    tasks = [ingest_task]
)