"""Models for various Databricks task types."""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pyjaws.api.base import BaseTask
from typing import ClassVar
import logging
import uuid
import os


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

    python_file: Optional[str] = ""
    local_module: Optional[Any] = None
    source: Source
    parameters: Optional[List[str]] = []
    _task_type: str = "spark_python_task"

    @field_validator("local_module")
    def verify_python_local_module(cls, v, info: FieldValidationInfo):
        logging.info(info.data.keys())
        python_file = info.data["python_file"]
        local_module = v
        logging.info(f"Python file: {python_file}")
        logging.info(f"Local module: {local_module}")

        if (
            ((python_file == "") and (not local_module))
            or ((python_file != "") and (local_module))
        ):
            raise ValueError(
                "Either python_file or local_module must be valid (not both)"
            )
        if local_module is not None:
            module_path = os.path.abspath(local_module.__file__)
            module_file_name = os.path.basename(module_path)
            logging.info(f"Local module path: {module_path}")
            logging.info(f"Module file name: {file_name}")
            dbfs_path = f"dbfs:/pyjaws/{uuid.uuid4()}/{module_file_name}"
            info.data["python_file"] = dbfs_path
            return module_path
    
#SparkPythonTask.model_rebuild()
