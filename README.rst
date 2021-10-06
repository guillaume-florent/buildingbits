************
buildingbits
************

Centralized project build logic

**buildingbits** solves the problem of maintaining the build logic of many projects.

Let's say you have 50 Python projects to maintain. You want to change the
base image for all Dockerfiles or change the options for the code linting for all 50
projects. You can manually modify 50 projects ... or you can use **buildingbits**.

How does it work
****************

Add the following lines in a script at the project root:

.. code-block:: shell

	curl https://raw.githubusercontent.com/guillaume-florent/buildingbits/main/buildingbits/buildingbits.py > buildingbits.py
	python buildingbits.py

or create a *Makefile* :

.. code-block:: shell

	buildingbits:
		curl https://raw.githubusercontent.com/guillaume-florent/buildingbits/main/buildingbits/buildingbits.py > buildingbits.py
		python buildingbits.py

and invoke the *buildingbits* target:

.. code-block:: shell

	make buildingbits


What does buildingbits.py do?
*****************************

* Download a *.prospector.yaml* file
* Download a *setup.py* file that will allow pre-PEP 517/518 setups to work (requires a setup.cfg)
* Download a Makefile template : *Makefile.template*
* Create a *Dockerfile* using a project local *Dockerfile.template* file and the files in *buildingbits/dockerfilebits*.
* Create a *.gitignore* using a project local *gitignore.template* and the files in *buildingbits/gitignorebits*
* Create a *Makefile* from the downloaded *Makefile.template* and the local project info (project name)

The name of the .txt files correspond to the tag that should be used in the templates.
e.g. use the {{ miniconda }} tag in a template to insert the content of *dockerfilebits/miniconda.txt* in a Dockerfile.

Best practices
**************

Call the *buildingbits* target (make) in a CI oriented Docker based build.

Dependencies
************

* make
* curl
* jinja2 (pip install jinja2)