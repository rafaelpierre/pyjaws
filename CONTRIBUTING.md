# PyJaws Contribution Guidelines

**PyJaws** welcomes contributions from the community.

This instructions are for linux base systems. (Linux, MacOS, BSD, etc.)
## Setting up your own fork of this repo.

- On github interface click on `Fork` button.
- Clone your fork of this repo. `git clone git@github.com:YOUR_GIT_USERNAME/project_urlname.git`
- Enter the directory `cd project_urlname`
- Add upstream repo `git remote add upstream https://github.com/author_name/project_urlname`

## Setting up your own virtual environment

We recommend `pyenv`.
Create a virtual environment by running `python -m venv .venv`.
Then activate it with `source .venv/bin/activate`.

## Install the project in develop mode

Run `pip install -e ./pyjaws`.

## Run the tests to ensure everything is working

Make sure the dependencies in `test-requirements.txt`, and run `tox`.

## Create a new branch to work on your contribution

Run `git checkout -b my_contribution`

## Make your changes

Edit the files using your preferred editor. (we recommend VIM or VSCode)

## Format the code

Run `tox -e fix` to format the code.

## Run the linter

Run `tox -e lint` to run the linter.

## Test your changes

Run `tox` to run the tests.

Ensure code coverage report shows at least `77%` coverage, add tests to your PR.

## Commit your changes

This project uses [conventional git commit messages](https://www.conventionalcommits.org/en/v1.0.0/).

Example: `fix(package): update setup.py arguments 🎉` (emojis are fine too)

## Push your changes to your fork

Run `git push origin my_contribution`

## Submit a pull request

On github interface, click on `Pull Request` button.

Wait CI to run and one of the developers will review your PR.