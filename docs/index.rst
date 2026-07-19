Perses API SDK
=============================

A Python SDK for the [Perses](https://perses.dev) API.

Requirements
------------

- Python 3.12+
- A running Perses instance

Installation
------------

Install the package via pip::

    pip install perses-api-sdk

Quick Start
-----------

Get started in just a few lines::

    from perses_api import APIModel, Project, Dashboard
    from perses_api.model import Metadata, ProjectSpec, DashboardSpec
    from perses_api.model import Project as ProjectModel, Dashboard as DashboardModel

    # Connect with a bearer token
    client = APIModel(host="http://localhost:8080", token="<your-token>")

    # Or connect with username/password (Basic auth)
    client = APIModel(host="http://localhost:8080", username="admin", password="password")

    # Create a project
    projects = Project(client)
    project = projects.create_project(
        ProjectModel(metadata=Metadata(name="my-project"), spec=ProjectSpec())
    )

    # Create a dashboard inside it
    dashboards = Dashboard(client)
    dashboard = dashboards.create_dashboard(
        "my-project",
        DashboardModel(
            metadata=Metadata(name="my-dashboard", project="my-project"),
            spec=DashboardSpec(),
        ),
    )

Perses API SDK
==============

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
