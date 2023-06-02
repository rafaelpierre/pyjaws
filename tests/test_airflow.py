from examples.airflow.sample_airflow_dag import dag
from pyjaws.pyjaws.airflow.conversion import convert_dag

import logging

logging.basicConfig(level = "DEBUG")

def test_airflow():
    result = convert_dag(dag)
    logging.error(result)
    logging.error(result.dag_id)
    logging.error(result.default_args)
    for task in result.tasks:
        if task.json:
            logging.error(task.json)
        logging.error(type(task))

    assert False

