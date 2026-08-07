# perses-api-sdk ![Coverage report](https://github.com/ZPascal/perses_api_sdk/blob/main/docs/coverage.svg)

A Python SDK for the [Perses](https://perses.dev) API.

## Requirements

- Python 3.12+
- A running Perses instance

## Installation

```bash
pip install perses-api-sdk
```

## Quick start

```python
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
```

## Authentication

Pass a bearer token via `token=`, or supply `username=` and `password=` for HTTP Basic auth. When both are provided, the token takes precedence.

```python
# Bearer token
client = APIModel(host="http://localhost:8080", token="eyJ...")

# Basic auth
client = APIModel(host="http://localhost:8080", username="admin", password="secret")
```

## Available clients

| Class | Scope | Description |
|---|---|---|
| `Project` | global | Projects |
| `Dashboard` | project | Dashboards |
| `EphemeralDashboard` | project | Ephemeral dashboards |
| `ProjectDatasource` | project | Datasources |
| `GlobalDatasource` | global | Global datasources |
| `ProjectVariable` | project | Variables |
| `GlobalVariable` | global | Global variables |
| `ProjectRole` | project | Roles |
| `GlobalRole` | global | Global roles |
| `ProjectRoleBinding` | project | Role bindings |
| `GlobalRoleBinding` | global | Global role bindings |
| `ProjectSecret` | project | Secrets |
| `GlobalSecret` | global | Global secrets |
| `User` | global | Users |
| `Plugin` | global | Plugin listing |
| `Migrate` | global | Grafana → Perses migration |
| `Validate` | global | Dashboard validation |

## Configuration options

```python
client = APIModel(
    host="http://localhost:8080",
    token="<token>",
    timeout=30.0,  # request timeout in seconds (default: 10)
    http2_support=False,  # enable HTTP/2 (requires httpx[http2])
    num_pools=10,  # max concurrent connections
    retries=False,  # retry failed requests
    follow_redirects=True,  # follow HTTP redirects
)
```

## Examples

### Datasource

```python
from perses_api import APIModel, ProjectDatasource
from perses_api.model import Metadata, DatasourceSpec, Datasource as DatasourceModel

client = APIModel(host="http://localhost:8080", token="<token>")
ds = ProjectDatasource(client, "my-project")

created = ds.create_datasource(
    DatasourceModel(
        metadata=Metadata(name="prometheus", project="my-project"),
        spec=DatasourceSpec(
            default=True,
            plugin={
                "kind": "PrometheusDatasource",
                "spec": {"directUrl": "http://prometheus:9090"},
            },
        ),
    )
)
```

### Migrate a Grafana dashboard

```python
from perses_api import APIModel, Migrate

client = APIModel(host="http://localhost:8080", token="<token>")
m = Migrate(client)

perses_dashboard = m.migrate(grafana_dashboard={"title": "My Dashboard", "panels": []})
```

### Validate a dashboard

```python
from perses_api import APIModel, Validate

client = APIModel(host="http://localhost:8080", token="<token>")
v = Validate(client)

v.validate(dashboard={"kind": "Dashboard", "metadata": {}, "spec": {}})
```

## Development

### Setup

```bash
# Install with test dependencies
uv sync --extra test

# Install with docs dependencies
uv sync --extra docs
```

### Running integration tests

Requires Docker.

```bash
make integration
```

Or against an existing Perses instance:

```bash
PERSES_HOST=http://localhost:8080 \
PERSES_USERNAME=admin \
PERSES_PASSWORD=password \
uv run pytest tests/integration/ -v
```

## License

[Apache 2.0](LICENSE)
