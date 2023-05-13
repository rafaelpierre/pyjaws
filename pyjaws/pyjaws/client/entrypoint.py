"""CLI Entrypoints for Workflows functionality."""

import importlib
import pathlib
import glob
import logging
import click
import os
import sys
from pyjaws.api import jobs


logging.basicConfig(level="DEBUG")


@click.group()
def app():
    click.echo("Main")
    pass


@click.command(name="create")
@click.argument("input_folder", type=str, default="./")
@click.option(
    "--overwrite",
    is_flag=True,
    show_default=True,
    default=True,
    help="Overwrite existing workflow.",
)
def create(input_folder: str, overwrite: bool = False):
    """
    Creates a Jobs Workflow for the Python job definitions stored in
    input_folder.

    Params:
        input_folder: Path to the input Python files.
    """

    try:
        logging.info("Starting workflow creation task")

        path = pathlib.Path(input_folder)
        target_path = f"{str(path)}/*.py"
        logging.info(f"Trying to parse all workflows from directory: {target_path}")
        target_scripts = [
            target for target in glob.glob(target_path) if "__init__.py" not in target
        ]
        logging.info(f"Found: {target_scripts}")

        for script_path in [
            target for target in target_scripts if "__init__.py" not in target
        ]:
            module_path = script_path.split(".py")[0]
            module_path = module_path.replace("/", ".")
            logging.info(f"Parsing script {module_path}...")
            logging.info(f"CWD: {os.getcwd()}")
            sys.path.append(os.getcwd())
            module = importlib.import_module(module_path)

            workflow = module.workflow
            logging.info(f"Imported workflow: {workflow.json()}")

            logging.info(f"Deploying job workflow for {script_path}...")
            jobs.create(workflow, overwrite)

        logging.info("Finished workflow creation task")
        return sys.exit(0)

    except Exception as exception:
        logging.error(f"Error deploying jobs: {str(exception)}")
        raise exception


app.add_command(name="create", cmd=create)


def main():
    app(standalone_mode=False)
