"""Models for various Databricks task types."""

from enum import Enum
from typing import Dict, List, Optional

from pyjaws.api.base import BaseTask


class Source(Enum):
    """Source for source code. "WORKSPACE" or "GIT" """

    WORKSPACE = "WORKSPACE"
    GIT = "GIT"


class PythonWheelTask(BaseTask):
    """Model for databricks python wheel task.

    Params:
        key (str): Task key\n
        cluster (Cluster): Cluster for running task\n
        dependencies (Optional[List[Task]]): An optional array of objects specifying the
            dependency graph of the task, defaults to None\n
        libraries Optional(List[dict]): List of Python libraries to be installed,
            defaults to None\n
        task_name (str): Task name\n
        package_name (str): Name of the package to execute\n
        entrypoint (str): Named entry point to use\n
        parameters (Optional[List[str]]): Command-line parameters, defaults to []\n
    """

    task_name: str
    package_name: str
    entrypoint: str
    parameters: Optional[List[str]] = []
    _task_type: str = "python_wheel_task"


class NotebookTask(BaseTask):
    """Model for databricks python notebook task.

    Params:
        key (str): Task key\n
        cluster (Cluster): Cluster for running task\n
        dependencies (Optional[List[Task]]): An optional array of objects specifying the
            dependency graph of the task, defaults to None\n
        libraries Optional(List[dict]): List of Python libraries to be installed,
            defaults to None\n
        notebook_path (str): The path of the notebook to be run\n
        source (Source): Source for source code\n
        base_parameters (Optional[Dict[str, int | str | float]]): key value parameters,
            defaults to {}\n
    """

    notebook_path: str
    source: Source
    base_parameters: Optional[Dict[str, int | str | float]] = {}
    _task_type: str = "notebook_task"


class SparkPythonTask(BaseTask):
    """Model for databricks spark python task.

    Params:
        key (str): Task key\n
        cluster (Cluster): Cluster for running task\n
        dependencies (Optional[List[Task]]): An optional array of objects specifying the
            dependency graph of the task, defaults to None\n
        libraries Optional(List[dict]): List of Python libraries to be installed,
            defaults to None\n
        python_file (str): The Python file to be executed\n
        source (Source): Source for source code\n
        parameters (Optional[List[str]]): Command-line parameters, defaults to []\n
    """

    python_file: str
    source: Source
    parameters: Optional[List[str]] = []
    _task_type: str = "spark_python_task"
