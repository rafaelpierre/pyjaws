from databricks.sdk import (
    WorkspaceClient,
    AccountClient
)

from databricks.sdk.core import ApiClient

from unittest import mock

from databricks.sdk.service.jobs import JobTaskSettings, JobCluster

from dotenv import load_dotenv

load_dotenv()

#@mock.patch(
#    "databricks.sdk.JobsAPI.create", mock.MagicMock()
#)
#@mock.patch.dict(
#    "os.environ",
#    {
#       "DATABRICKS_HOST": "test_host",
#        "DATABRICKS_TOKEN": "test_token",
#    },
#)
def test_jobs():

    from databricks.sdk import JobsAPI

    client = ApiClient()
    api = JobsAPI(client)
    cluster = JobCluster(
        job_cluster_key = "cluster1"
    )

    task1 = JobTaskSettings(
        task_key = "task1",
    )

    api.create(
        job_clusters = [cluster],
        tasks = [task1]
    )

    #api.create.assert_called_once()
