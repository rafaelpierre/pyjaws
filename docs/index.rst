.. meta::
      :google-site-verification: "3wBiq9Skr01hUP4Vfwl_Rpo7RSnRiyiXmYihUWgPgug"

🦈 pyjaws
==================

* **PyJaws** enables declaring Databricks Jobs and Workflows as Python code, allowing for code Linting, Formatting, Parameter Validation, Modularity and reusability.
* In addition to those, PyJaws also provides some nice features such as **cycle detection** out of the box.

Folks who have used Python-based orchestration tools such as **Apache Airflow**, **Luigi** and **Mage** will be familiar with the concepts and the API if **PyJaws**.

.. image:: https://raw.githubusercontent.com/rafaelpierre/pyjaws/main/img/pyjaws.png
  :width: 600
  :alt: PyJaws Mascot - A Shark on Steroids!
  :align: center

Project Homepage
----------------

* `Github Repo <https://www.github.com/rafaelpierre/pyjaws>`_
* `PyPi.org Project <https://pypi.org/project/pyjaws>`_

Getting Started
---------------


* First step is installing pyjaws: ::

   pip install pyjaws

* Once it's installed, define your Databricks Workspace authentication variables: ::

   export DATABRICKS_HOST = ...
   export DATABRICKS_TOKEN = ...

Last, define your Workflow Tasks (see examples) and run: ::

   pyjaws create path/to/your/workflow_definitions

Sample Job Definition
---------------------

Below you can find a simple PyJaws job definition: ::

   from pyjaws.api.base import (
      Cluster,
      Runtime,
      Workflow
   )
   from pyjaws.api.tasks import PythonWheelTask

   cluster = Cluster(
      job_cluster_key = "ai_cluster",
      spark_version = Runtime.DBR_13_ML,
      num_workers = 2,
      node_type_id = "Standard_DS3_v2",
      cluster_log_conf = {
         "dbfs": {
               "destination": "dbfs:/home/cluster_log"
         }
      }
   )


   # Create a Task object.

   ingest_task = PythonWheelTask(
      key = "ingest",
      cluster = cluster,
      entrypoint = "iot",
      task_name = "ingest",
      parameters = [
         f"my_parameter_value",
         "--output-table", "my_table"
      ]
   )

   transform_task = PythonWheelTask(
      key = "transform",
      cluster = cluster,
      entrypoint = "iot",
      task_name = "ingest",
      dependencies = [ingest_task],
      parameters = [
         f"my_parameter_value2",
         "--input-table", "my_table"
         "--output-table", "output_table"
      ]
   )


   # Create a Workflow object to define dependencies
   # between previously defined tasks.

   workflow = Workflow(
      name = "my_workflow",
      tasks = [ingest_task, transform_task]
   )

API Reference
-------------

If you are looking for information on a specific function, class, or
method, this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api