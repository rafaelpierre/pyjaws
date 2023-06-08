"""Base class for PyJaws Databricks Jobs & Workflows."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from json.decoder import JSONDecodeError
from threading import Lock
from typing import List, Optional

import git
import jinja2
import networkx as nx
import rapidjson
from matplotlib import pyplot as plt
from pydantic import BaseModel

from pyjaws import __version__
from pyjaws.api.runtime import Runtime

BASE_PATH = os.path.dirname(__file__)


class Cluster(BaseModel):
    job_cluster_key: str
    spark_version: Runtime
    num_workers: int
    node_type_id: Optional[str] = None
    autoscale: Optional[bool] = None
    instance_pool_id: Optional[str] = None
    runtime_engine: Optional[str] = None
    cluster_log_conf: Optional[dict] = None
    __cluster: List[Cluster] = []  # mutable list to store current instance
    __lock: Lock = Lock()  # to prevent race conditions

    def __init__(self, **kwargs):
        """
        Creates a cluster object.
        Params:
            job_cluster_key (str): Job Cluster identifying key.\n
            spark_version (pyjaws.api.base.Cluster): Spark Cluster Runtime.\n
            num_workers (int): Number of workers in the cluster.\n
            node_type_id (int): Type of VM to use for Driver and Workers.\n
            autoscale (bool): Enable autoscaling.\n
            instance_pool_id (str): Specify an Instance Pool for the job cluster.\n
            runtime_engine: (str): STANDARD or PHOTON.\n
            cluster_lob_conf (dict): Dict containing configurations for
            storing cluster logs.\n
        """
        super().__init__(**kwargs)

    def __str__(self):
        return self.job_cluster_key

    def __enter__(self) -> Cluster:
        """Injects cluster instance into tasks created within context manger syntax."""
        if self.__cluster:
            raise Exception("Nested clusters are not supported!!")
        self.__lock.acquire()
        self.__cluster.append(self)
        return self

    def __exit__(self, *args):
        self.__cluster.pop()
        self.__lock.release()

    @classmethod
    def _get_cluster(cls) -> Cluster:
        """A helper method to return the cluster instance."""
        if cls.__cluster:
            return cls.__cluster[-1]
        else:
            raise Exception("_get_cluster cannot be called outside of with clause!!")

    @property
    def cluster_log_conf_str(self) -> str:
        return json.dumps(self.cluster_log_conf)


class BaseTask(BaseModel):
    """
    Base class for Databricks Workflow Task.
    Params:
        key: Task key.
        cluster: Cluster object for running the task.
        libraries: List of Python libraries to be installed.
    """

    key: str
    cluster: Optional[Cluster] = None
    dependencies: Optional[List[BaseTask]] = []
    libraries: Optional[List[dict]] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.cluster and Cluster._get_cluster():
            self.cluster = Cluster._get_cluster()

    def __str__(self):
        return self.key

    def set_relatives(self, downstream, task_or_task_list):
        if isinstance(task_or_task_list, list):
            for task in task_or_task_list:
                self.set_relatives(downstream=downstream, task_or_task_list=task)
        elif downstream:
            self.dependencies.append(task_or_task_list)
        else:
            # Upstream
            task_or_task_list.dependencies.append(self)

    def __lshift__(self, task_or_task_list):
        self.set_relatives(downstream=True, task_or_task_list=task_or_task_list)

    def __rshift__(self, task_or_task_list):
        self.set_relatives(downstream=False, task_or_task_list=task_or_task_list)


class Workflow(BaseModel):
    """
    Base class for PyJaws Databricks Workflow.
    Params:
        name: Workflow name.
        tasks: List of Workflow Tasks.
    """

    class Config:
        arbitrary_types_allowed = True

    name: str
    tasks: List[BaseTask]
    tags: Optional[dict] = {}
    graph: nx.Graph = None
    schedule: Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._create_graph()
        self.validate()
        self._set_tags(kwargs.get("tags", {}))

    def _set_tags(self, tags):
        self.tags = {
            "pyjaws_version": __version__,
            "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.tags.update(tags)

        try:
            repo = git.Repo(search_parent_directories=True)

            commit_hash = repo.head.object.hexsha
            branch = repo.active_branch.name
            origin = repo.remote("origin").url

            repo_tags = {
                "commit_hash": commit_hash if commit_hash else "NA",
                "branch": branch if branch else "NA",
                "origin": origin,
            }

        except Exception as exception:
            logging.error(f"Exception: {str(exception)}")
            logging.error("No git repo found")

            repo_tags = {
                "commit_hash": "NA",
                "branch": "NA",
                "origin": "NA",
            }

        self.tags.update(repo_tags)

    @property
    def clusters(self) -> dict:
        clusters = [task.cluster for task in self.tasks]
        unique_clusters = {}
        for cluster in clusters:
            unique_clusters[str(cluster)] = cluster

        return unique_clusters

    def json(
        self,
        search_path=f"{BASE_PATH}/templates",
        template_file="workflow.j2",
    ):
        try:
            with open(f"{search_path}/{template_file}", "r"):
                loader = jinja2.FileSystemLoader(searchpath=search_path)
                env = jinja2.Environment(loader=loader)
                workflow_template = template_file
                template = env.get_template(workflow_template)
                result = template.render(workflow=self)
                result_json = rapidjson.loads(
                    result, parse_mode=rapidjson.PM_TRAILING_COMMAS
                )
                return result_json

        except JSONDecodeError as exception:
            logging.error(f"Error parsing JSON: {result}")
            raise exception

    def _validate_tasks(self):
        task_keys = [task.key for task in self.tasks]
        unique_task_keys = set(task_keys)

        if len(task_keys) > len(unique_task_keys):
            raise ValueError("Task keys cannot be repeated in a workflow")

        for task in self.tasks:
            if task.cluster.job_cluster_key not in [
                str(cluster) for cluster in self.clusters
            ]:
                raise ValueError(f"Invalid Cluster ID: {task.cluster.job_cluster_key}")

    def _create_graph(self):
        edge_list = []

        if len(self.tasks) == 1:
            self.graph = nx.Graph()
            self.graph.add_node(self.tasks[0].task_name)
        else:
            for task in self.tasks:
                for dependency in task.dependencies or []:
                    edge_list.append((str(dependency), str(task)))

            self.graph = nx.DiGraph(edge_list)

    def _validate_cycles(self):
        cycles = list(nx.simple_cycles(self.graph))
        if len(cycles) > 0:
            raise ValueError("Cycle(s) detected in the workflow")

    def validate(self):
        super().validate(self)
        self._validate_tasks()
        self._validate_cycles()

    def _ipython_display_(self):
        nx.draw(self.graph, with_labels=True)
        plt.show()
