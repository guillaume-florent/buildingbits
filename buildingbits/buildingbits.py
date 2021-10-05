#!/usr/bin/env python
# coding: utf-8

r"""Buildingbits script."""

import os
import urllib.request
from os.path import basename

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

SUPPORTED_DOCKERFILE_KEYS = [
    "base",
    "miniconda",
    "occ_0.18",
    "occ_7.5",
    "common_infrastructure",
]
SUPPORTED_GITIGNORE_KEYS = [
    "generic",
    "python",
    "pycharm",
    "pytest",
    "pytest_cov",
    "pytest_benchmark",
    "mypy",
]


def trace(msg):
    r"""Print a trace."""
    print(msg)


def download(url: str, file_name: str) -> None:
    r"""Download a file."""
    with urllib.request.urlopen(url) as response, open(file_name, "wb") as out_file:
        data = response.read()  # a `bytes` object
        out_file.write(data)


def file_from_template(keys, url, template_name, output_file):
    r"""Create a file using the definitions in url + key and the provided template."""
    d = {}
    for k in keys:
        trace(f"Reading : {url}/{k}.txt")
        d[k] = urllib.request.urlopen(f"{url}/{k}.txt").read().decode("utf-8")

    file_loader = FileSystemLoader(".")  # directory of template file
    env = Environment(loader=file_loader)

    template = env.get_template(template_name)  # load template file
    output = template.render(**d)
    with open(output_file, "w", encoding="utf-8") as file_:
        file_.write(output)


if __name__ == "__main__":
    # download .prospector.yaml
    trace("Downloading .prospector.yaml ...")
    download(PROSPECTOR_YAML_URL, PROSPECTOR_YAML_FILENAME)
    trace(" ... done.")

    # download setup.py
    trace("Downloading setup.py ...")
    download(SETUP_PY_URL, SETUP_PY_FILENAME)
    trace(" ... done.")

    # download Makefile.template
    trace("Downloading Makefile.template ...")
    download(MAKEFILE_TEMPLATE_URL, MAKEFILE_TEMPLATE_FILENAME)
    trace(" ... done.")

    # create Dockerfile from local template
    trace("Creating Dockerfile from template ...")
    file_from_template(
        keys=SUPPORTED_DOCKERFILE_KEYS,
        url=DOCKERFILEBITS_URL,
        template_name="Dockerfile.template",
        output_file="Dockerfile",
    )
    trace(" ... done.")

    # create .gitignore from local template
    trace("Creating .gitignore from template ...")
    file_from_template(
        keys=SUPPORTED_GITIGNORE_KEYS,
        url=GITIGNOREBITS_URL,
        template_name="gitignore.template",
        output_file=".gitignore",
    )
    trace(" ... done.")

    # overwrite the initial Makefile
    trace("Creating a new Makefile from template ...")
    file_loader = FileSystemLoader(".")  # directory of template file
    env = Environment(loader=file_loader)

    template = env.get_template("Makefile.template")  # load template file
    project_name = basename(os.getcwd())
    trace(f"Project name: {project_name}")
    output = template.render(project_name=project_name)
    with open("Makefile", "w", encoding="utf-8") as file_:
        file_.write(output)
    trace(" ... done.")
