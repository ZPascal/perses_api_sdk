import uuid
from perses_api import (
    Project,
    Dashboard,
    ProjectDatasource,
    ProjectVariable,
    ProjectRole,
    User,
    Plugin,
)
from perses_api.model import (
    Metadata,
    ProjectSpec,
    Project as ProjectModel,
    DashboardSpec,
    Dashboard as DashboardModel,
    DatasourceSpec,
    Datasource as DatasourceModel,
    VariableSpec,
    Variable as VariableModel,
    RoleSpec,
    Permission,
    Role as RoleModel,
    UserSpec,
    User as UserModel,
)


def unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def unique_id(prefix: str) -> str:
    """Like unique() but uses underscores — required for resource names that forbid hyphens (e.g. variables)."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def test_project_crud(perses_client):
    client = Project(perses_client)
    name = unique("sdk-test-project")

    created = client.create_project(
        ProjectModel(metadata=Metadata(name=name), spec=ProjectSpec())
    )
    assert created["metadata"]["name"] == name

    fetched = client.get_project(name)
    assert fetched["metadata"]["name"] == name

    projects = client.get_projects()
    names = [p["metadata"]["name"] for p in projects]
    assert name in names

    updated = client.update_project(
        name,
        ProjectModel(
            metadata=Metadata(name=name), spec=ProjectSpec(display={"name": "Updated"})
        ),
    )
    assert updated["metadata"]["name"] == name

    client.delete_project(name)

    remaining = client.get_projects()
    assert name not in [p["metadata"]["name"] for p in remaining]


def test_dashboard_crud(perses_client):
    project_client = Project(perses_client)
    project_name = unique("sdk-dash-proj")
    project_client.create_project(
        ProjectModel(metadata=Metadata(name=project_name), spec=ProjectSpec())
    )

    client = Dashboard(perses_client)
    dash_name = unique("sdk-dash")

    created = client.create_dashboard(
        project_name,
        DashboardModel(
            metadata=Metadata(name=dash_name, project=project_name),
            spec=DashboardSpec(),
        ),
    )
    assert created["metadata"]["name"] == dash_name

    fetched = client.get_dashboard(project_name, dash_name)
    assert fetched["metadata"]["name"] == dash_name

    dashboards = client.get_dashboards(project_name)
    assert any(d["metadata"]["name"] == dash_name for d in dashboards)

    updated = client.update_dashboard(
        project_name,
        dash_name,
        DashboardModel(
            metadata=Metadata(name=dash_name, project=project_name),
            spec=DashboardSpec(duration="5m"),
        ),
    )
    assert updated["metadata"]["name"] == dash_name

    client.delete_dashboard(project_name, dash_name)
    project_client.delete_project(project_name)


def test_datasource_crud(perses_client):
    project_client = Project(perses_client)
    project_name = unique("sdk-ds-proj")
    project_client.create_project(
        ProjectModel(metadata=Metadata(name=project_name), spec=ProjectSpec())
    )

    client = ProjectDatasource(perses_client, project_name)
    ds_name = unique("sdk-ds")
    plugin = {
        "kind": "PrometheusDatasource",
        "spec": {"directUrl": "http://prometheus:9090"},
    }

    created = client.create_datasource(
        DatasourceModel(
            metadata=Metadata(name=ds_name, project=project_name),
            spec=DatasourceSpec(default=False, plugin=plugin),
        )
    )
    assert created["metadata"]["name"] == ds_name

    fetched = client.get_datasource(ds_name)
    assert fetched["metadata"]["name"] == ds_name

    datasources = client.get_datasources()
    assert any(d["metadata"]["name"] == ds_name for d in datasources)

    updated = client.update_datasource(
        ds_name,
        DatasourceModel(
            metadata=Metadata(name=ds_name, project=project_name),
            spec=DatasourceSpec(default=True, plugin=plugin),
        ),
    )
    assert updated["metadata"]["name"] == ds_name

    client.delete_datasource(ds_name)
    project_client.delete_project(project_name)


def test_variable_crud(perses_client):
    project_client = Project(perses_client)
    project_name = unique("sdk-var-proj")
    project_client.create_project(
        ProjectModel(metadata=Metadata(name=project_name), spec=ProjectSpec())
    )

    client = ProjectVariable(perses_client, project_name)
    var_name = unique_id("sdk_var")

    created = client.create_variable(
        VariableModel(
            metadata=Metadata(name=var_name, project=project_name),
            spec=VariableSpec(
                kind="TextVariable", spec={"value": "hello", "constant": False}
            ),
        )
    )
    assert created["metadata"]["name"] == var_name

    fetched = client.get_variable(var_name)
    assert fetched["metadata"]["name"] == var_name

    variables = client.get_variables()
    assert any(v["metadata"]["name"] == var_name for v in variables)

    updated = client.update_variable(
        var_name,
        VariableModel(
            metadata=Metadata(name=var_name, project=project_name),
            spec=VariableSpec(
                kind="TextVariable", spec={"value": "world", "constant": False}
            ),
        ),
    )
    assert updated["metadata"]["name"] == var_name

    client.delete_variable(var_name)
    project_client.delete_project(project_name)


def test_role_crud(perses_client):
    project_client = Project(perses_client)
    project_name = unique("sdk-role-proj")
    project_client.create_project(
        ProjectModel(metadata=Metadata(name=project_name), spec=ProjectSpec())
    )

    client = ProjectRole(perses_client, project_name)
    role_name = unique("sdk-role")

    created = client.create_role(
        RoleModel(
            metadata=Metadata(name=role_name, project=project_name),
            spec=RoleSpec(
                permissions=[Permission(actions=["read"], scopes=["Dashboard"])]
            ),
        )
    )
    assert created["metadata"]["name"] == role_name

    fetched = client.get_role(role_name)
    assert fetched["metadata"]["name"] == role_name

    roles = client.get_roles()
    assert any(r["metadata"]["name"] == role_name for r in roles)

    updated = client.update_role(
        role_name,
        RoleModel(
            metadata=Metadata(name=role_name, project=project_name),
            spec=RoleSpec(
                permissions=[
                    Permission(actions=["read", "create"], scopes=["Dashboard"])
                ]
            ),
        ),
    )
    assert updated["metadata"]["name"] == role_name

    client.delete_role(role_name)
    project_client.delete_project(project_name)


def test_user_crud(perses_client):
    client = User(perses_client)
    username = unique("sdk-user")

    created = client.create_user(
        UserModel(
            metadata=Metadata(name=username),
            spec=UserSpec(
                first_name="Test",
                last_name="User",
                native_provider={"password": "test123!"},
            ),
        )
    )
    assert created["metadata"]["name"] == username

    fetched = client.get_user(username)
    assert fetched["metadata"]["name"] == username

    users = client.get_users()
    assert any(u["metadata"]["name"] == username for u in users)

    updated = client.update_user(
        username,
        UserModel(
            metadata=Metadata(name=username),
            spec=UserSpec(first_name="Updated", last_name="User"),
        ),
    )
    assert updated["metadata"]["name"] == username

    client.delete_user(username)


def test_get_plugins(perses_client):
    client = Plugin(perses_client)
    result = client.get_plugins()
    assert isinstance(result, list)
