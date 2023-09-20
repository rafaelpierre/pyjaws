import logging
import json
from databricks.sdk.service.jobs import JobsAPI, JobSettings, JobCluster, Task
from databricks.sdk.core import ApiClient
import traceback

from pyjaws.api.base import Workflow

API_VERSION = "2.1"


def create(workflow: Workflow, overwrite: bool = False):
    logging.info(f"Workflow: {workflow}")
    json_workflow = json.dumps(workflow.json())
    logging.info(f"Creating workflow: {json_workflow}")

    try:
        api_client = ApiClient()
        logging.info("Deploying jobs...")
        jobs_api = JobsAPI(api_client)
        existing_jobs = list(jobs_api.list(name=workflow.name))
        dict_settings = workflow.json()
        JobSettings(**dict_settings)
        logging.info(f"Found existing jobs: {existing_jobs}")
        dict_settings["job_clusters"] = [
            JobCluster.from_dict(cluster) for cluster in dict_settings["job_clusters"]
        ]
        dict_settings["tasks"] = [
            Task.from_dict(task) for task in dict_settings["tasks"]
        ]

        if overwrite and len(existing_jobs) > 0:
            for job in existing_jobs:
                logging.info(f"Resetting job: {job}")
                jobs_api.reset(
                    job_id=job.job_id, new_settings=JobSettings(**dict_settings)
                )
        else:
            logging.info("Creating job")
            logging.info(f"Settings: {dict_settings}")

            jobs_api.create(**dict_settings)

        return dict_settings

    except Exception as exception:
        logging.error("Error creating Databricks Jobs Workflow:")
        logging.error(str(exception))
        traceback.print_exc()
