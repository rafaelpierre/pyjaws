import logging
import json
import os
from databricks_cli.jobs.api import JobsApi
from databricks_cli.sdk import ApiClient

from pyjaws.api.base import Workflow

API_VERSION = "2.1"


def create(workflow: Workflow, overwrite: bool = False):
    logging.info(f"Workflow: {workflow}")
    json_workflow = json.dumps(workflow.json())
    logging.info(f"Creating workflow: {json_workflow}")

    try:
        api_client = ApiClient(
            host=os.environ["DATABRICKS_HOST"],
            token=os.environ["DATABRICKS_TOKEN"],
        )
        logging.info(f"Deploying jobs to {os.environ['DATABRICKS_HOST']}")
        result = None
        jobs_api = JobsApi(api_client)
        existing_jobs = jobs_api._list_jobs_by_name(name=workflow.name)

        if overwrite and existing_jobs:
            for job in existing_jobs:
                json_ = {
                    "job_id": job["job_id"],
                    "new_settings": workflow.json(),
                }
                logging.info(f"Reseting job: {job}")
                result = jobs_api.reset_job(json=json_, version=API_VERSION)
        else:
            result = jobs_api.create_job(json=workflow.json(), version=API_VERSION)

        logging.info(f"Result: {str(result)}")
        return result

    except Exception as exception:
        logging.error("Error creating Databricks Jobs Workflow:")
        logging.error(str(exception))
