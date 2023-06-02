
ingest_task = PythonWheelTask(
    key="test1",
    cluster=cluster,
    package_name="my_package",
    entrypoint="ingest",
    task_name="ingest",
    libraries=[{"pypi": {"package": "deepspeed"}}],
    parameters=["my_parameter_value", "--output-table", "my_table"],
)