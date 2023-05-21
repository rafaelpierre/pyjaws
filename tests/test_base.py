from pyjaws.pyjaws.api.base import BaseTask
from tests.fixtures.job import cluster
import logging

logging.basicConfig(level = "DEBUG")

def test_lshift(cluster):

    task1 = BaseTask(
        key = "sample_task",
        cluster = cluster
    )

    task2 = BaseTask(
        key = "sample_task2",
        cluster = cluster
    )

    task2 << task1

    assert task2.dependencies == [task1]


def test_rshift(cluster):

    task1 = BaseTask(
        key = "sample_task",
        cluster = cluster
    )

    task2 = BaseTask(
        key = "sample_task2",
        cluster = cluster
    )

    task1 >> task2

    assert task2.dependencies == [task1]

