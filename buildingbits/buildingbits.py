#!/usr/bin/env python
# coding: utf-8

r"""Buildingbits script."""

import os
import urllib.request
from os.path import basename, isfile
from typing import Optional

from jinja2 import Environment, FileSystemLoader

URL = "https://raw.githubusercontent.com/guillaume-florent/buildingbits/main"
FILES_URL = f"{URL}/files"
DOCKERFILEBITS_URL = f"{URL}/dockerfilebits"
GITIGNOREBITS_URL = f"{URL}/gitignorebits"

PROSPECTOR_YAML_FILENAME = ".prospector.yaml"
PROSPECTOR_YAML_URL = f"{FILES_URL}/{PROSPECTOR_YAML_FILENAME}"

SETUP_PY_FILENAME = "setup.py"
SETUP_PY_URL = f"{FILES_URL}/{SETUP_PY_FILENAME}"

MAKEFILE_TEMPLATE_FILENAME = "Makefile.template"
MAKEFILE_TEMPLATE_URL = f"{FILES_URL}/{MAKEFILE_TEMPLATE_FILENAME}"

# These should be in sync with the contents of the dockerfilebits folder
SUPPORTED_DOCKERFILE_KEYS = [
    "base",
    "miniconda",
    "occ_0.18",
    "occ_7.5",
    "common_infrastructure",
]
# These should be in sync with the contents of the gitignorebits folder
SUPPORTED_GITIGNORE_KEYS = [
    "generic",
    "python",
    "pycharm",
    "pytest",
    "pytest_cov",
    "pytest_benchmark",
    "mypy",
]


class Colors:
    r"""Colors and font effects definitions."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def trace(msg: str, color: Optional[str] = None):
    r"""Print a trace."""
    if color is not None:
        print(f"{color}{msg}{Colors.ENDC}")
    else:
        print(msg)


def download(url: str, file_name: str) -> None:
    r"""Download a file."""
    trace(f"Downloading {file_name} from {url} ...")
    with urllib.request.urlopen(url) as response, open(file_name, "wb") as out_file:
        data = response.read()  # a `bytes` object
        out_file.write(data)
    trace(" ... done.", color=Colors.OKGREEN)


def remote_tags(keys: list, url: str) -> dict:
    r"""Retrieve tag values."""
    trace(f"Retrieving tags from {url} ...")
    tags_kv = {}
    for k in keys:
        trace(f"Reading : {url}/{k}.txt")
        tags_kv[k] = urllib.request.urlopen(f"{url}/{k}.txt").read().decode("utf-8")
    return tags_kv


def do_template(tags: dict, template_name: str, output_file: str) -> None:
    r"""Perform templating."""
    trace(f"Templating {template_name} to produce {output_file} ...")
    file_loader = FileSystemLoader(".")  # directory of template file
    env = Environment(loader=file_loader)
    template = env.get_template(template_name)  # load template file
    output = template.render(**tags)
    with open(output_file, "w", encoding="utf-8") as file_:
        file_.write(output)
    trace(" ... done.", color=Colors.OKGREEN)


if __name__ == "__main__":
    trace("******** .prospector.yaml ********", color=Colors.HEADER)
    if isfile(PROSPECTOR_YAML_FILENAME):
        trace(f"{PROSPECTOR_YAML_FILENAME} exists and would be overwritten", color=Colors.WARNING)
        trace("Nothing done.", color=Colors.WARNING)
        trace(f"Rename or remove the existing {PROSPECTOR_YAML_FILENAME} to have it replaced by the remote version.",
              color=Colors.OKBLUE)
    else:
        download(PROSPECTOR_YAML_URL, PROSPECTOR_YAML_FILENAME)

    trace("******** setup.py ********", color=Colors.HEADER)
    if isfile(SETUP_PY_FILENAME):
        trace(f"{SETUP_PY_FILENAME} exists and would be overwritten", color=Colors.WARNING)
        trace("Nothing done.", color=Colors.WARNING)
        trace(f"Rename or remove the existing {SETUP_PY_FILENAME} to have it replaced by the remote version.",
              color=Colors.OKBLUE)
    else:
        download(SETUP_PY_URL, SETUP_PY_FILENAME)

    trace("******** Makefile.template ********", color=Colors.HEADER)
    if isfile(MAKEFILE_TEMPLATE_FILENAME):
        trace(f"{MAKEFILE_TEMPLATE_FILENAME} exists and would be overwritten", color=Colors.WARNING)
        trace("Nothing done.", color=Colors.WARNING)
        trace(f"Rename or remove the existing {MAKEFILE_TEMPLATE_FILENAME} to have it replaced by the remote version.",
              color=Colors.OKBLUE)
    else:
        download(MAKEFILE_TEMPLATE_URL, MAKEFILE_TEMPLATE_FILENAME)

    trace("******** Dockerfile from Dockerfile.template ********", color=Colors.HEADER)
    if isfile("Dockerfile.template"):
        dockerfile_tags = remote_tags(SUPPORTED_DOCKERFILE_KEYS, DOCKERFILEBITS_URL)
        do_template(dockerfile_tags, "Dockerfile.template", "Dockerfile")
    else:
        trace("No Dockerfile.template found. Is that intentional?", color=Colors.WARNING)

    trace("******** .gitignore from gitignore.template ********", color=Colors.HEADER)
    if isfile("gitignore.template"):
        gitignore_tags = remote_tags(SUPPORTED_GITIGNORE_KEYS, GITIGNOREBITS_URL)
        do_template(gitignore_tags, "gitignore.template", ".gitignore")
    else:
        trace("No gitignore.template found. Is that intentional?", color=Colors.WARNING)

    trace("******** Makefile from (downloaded) Makefile.template ********", color=Colors.HEADER)
    if isfile("Makefile.template"):
        project_name = basename(os.getcwd())
        trace(f"Project name: {project_name}")
        tags_data = {"project_name": project_name}
        do_template(tags_data, "Makefile.template", "Makefile")
    else:
        trace("No Makefile.template found. How could that even happen?", color=Colors.FAIL)
