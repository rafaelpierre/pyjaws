from setuptools import find_packages, setup
import pyjaws
from pathlib import Path

PACKAGE_REQUIREMENTS = [
    "click",
    "python-rapidjson==1.10",
    "pydantic==1.10.5",
    "Jinja2==3.1.2",
    "networkx",
    "GitPython==3.1.31",
    "databricks-cli==0.17.5",
    "requests<2.30.0",
    "urllib3<2",
    "matplotlib",
]

current_dir = Path(__file__).parent.parent
long_description = (current_dir / "README.md").read_text()

setup(
    name="pyjaws",
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["README.md", "api/templates/*.j2", "api/templates/macros/*.j2"]},
    setup_requires=["setuptools", "wheel"],
    install_requires=PACKAGE_REQUIREMENTS,
    entry_points={"console_scripts": ["pyjaws = pyjaws.client.entrypoint:main"]},
    version=pyjaws.__version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Rafael Pierre",
)
