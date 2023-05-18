import logging
from unittest import mock

import pytest
from databricks_cli.jobs.api import JobsApi
from pyjaws.api import jobs

from tests.fixtures.job import (
    workflow_fixture,
    workflow_fixture_no_tags,
    workflow_multiple_cluster,
)


@mock.patch.object(
    JobsApi, "_list_jobs_by_name", mock.Mock(return_value=[{"job_id": "1234"}])
)
@mock.patch.object(JobsApi, "reset_job", mock.Mock(return_value={}))
@mock.patch.dict(
    "os.environ",
    {
        "DATABRICKS_HOST": "test_host",
        "DATABRICKS_TOKEN": "test_token",
    },
)
@pytest.mark.parametrize(
    "workflow_fixture_",
    ["workflow_fixture", "workflow_multiple_cluster"],
)
def test_overwrite_job(workflow_fixture_, request):
    """Test for create_job."""

    workflow = request.getfixturevalue(workflow_fixture_)
    result = jobs.create(workflow=workflow, overwrite=True)

    logging.info(f"Create result: {result}")
    assert isinstance(result, dict)


@mock.patch.object(JobsApi, "_list_jobs_by_name", mock.Mock(return_value=[]))
@mock.patch.object(JobsApi, "create_job", mock.Mock(return_value={"job_id": "123"}))
@mock.patch.dict(
    "os.environ",
    {
        "DATABRICKS_HOST": "test_host",
        "DATABRICKS_TOKEN": "test_token",
    },
)
@pytest.mark.parametrize(
    "workflow_fixture_",
    ["workflow_fixture", "workflow_multiple_cluster"],
)
def test_create_job(workflow_fixture_, request):
    """Test for create_job."""

    workflow = request.getfixturevalue(workflow_fixture_)
    logging.info(workflow.json())

    result = jobs.create(workflow=workflow, overwrite=True)

    logging.info(f"Create result: {result}")
    assert result
    assert result["job_id"]


def test_custom_tags(workflow_fixture):
    logging.info(workflow_fixture.tags)
    assert "test" in workflow_fixture.tags.keys()


@mock.patch.object(JobsApi, "_list_jobs_by_name", mock.Mock(return_value=[]))
@mock.patch.object(JobsApi, "create_job", mock.Mock(return_value={"job_id": "123"}))
@mock.patch.dict(
    "os.environ",
    {
        "DATABRICKS_HOST": "test_host",
        "DATABRICKS_TOKEN": "test_token",
    },
)
def test_create_no_tags(workflow_fixture_no_tags):
    """Test for create_job."""

    result = jobs.create(workflow=workflow_fixture_no_tags, overwrite=True)

    logging.info(f"Create result: {result}")
    assert result
    assert result["job_id"]
