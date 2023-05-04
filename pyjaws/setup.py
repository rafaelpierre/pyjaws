from setuptools import find_packages, setup
import pyjaws

PACKAGE_REQUIREMENTS = [
    "click",
    "python-rapidjson==1.10",
    "pydantic==1.10.5",
    "Jinja2==3.1.2",
    "networkx",
    "GitPython==3.1.31",
    "databricks-cli"
]

setup(
    name = "pyjaws",
    packages = find_packages(),
    include_package_data=True,
    setup_requires = ["setuptools", "wheel"],
    install_requires = PACKAGE_REQUIREMENTS,
    entry_points = {"console_scripts": ["pyjaws = pyjaws.client.entrypoint:main"]},
    version = pyjaws.__version__,
    description = "A Pythoninc Framework for Defining and Deploying Databricks Jobs & Workflows",
    author = "Rafael Pierre",
)
