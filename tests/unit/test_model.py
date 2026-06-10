import pytest
from perses_api.model import (
    APIModel,
    RequestsMethods,
    APIEndpoints,
    Metadata,
    Project,
    ProjectSpec,
    Dashboard,
    DashboardSpec,
    EphemeralDashboard,
    EphemeralDashboardSpec,
    Datasource,
    DatasourceSpec,
    Variable,
    VariableSpec,
    Role,
    RoleSpec,
    RoleBinding,
    RoleBindingSpec,
    Secret,
    SecretSpec,
    User,
    UserSpec,
)


def test_api_model_defaults():
    model = APIModel(host="http://localhost:8080")
    assert model.token is None
    assert model.timeout == 10.0
    assert model.http2_support is False
    assert model.num_pools == 10
    assert model.retries is False
    assert model.follow_redirects is True


def test_api_model_with_token():
    model = APIModel(host="http://localhost:8080", token="mytoken")
    assert model.token == "mytoken"


def test_api_model_with_basic_auth():
    model = APIModel(host="http://localhost:8080", username="admin", password="secret")
    assert model.username == "admin"
    assert model.password == "secret"


def test_requests_methods_values():
    assert RequestsMethods.GET.value == "GET"
    assert RequestsMethods.POST.value == "POST"
    assert RequestsMethods.PUT.value == "PUT"
    assert RequestsMethods.DELETE.value == "DELETE"


def test_api_endpoints_projects():
    assert APIEndpoints.PROJECTS.value == "/api/v1/projects"
    assert APIEndpoints.DASHBOARDS.value == "/api/v1/projects/{project}/dashboards"
    assert APIEndpoints.GLOBAL_DATASOURCES.value == "/api/v1/globaldatasources"
    assert APIEndpoints.MIGRATE.value == "/api/migrate"
    assert APIEndpoints.VALIDATE.value == "/api/validate/{resource_type}"


def test_metadata_required_name():
    m = Metadata(name="my-resource")
    assert m.name == "my-resource"
    assert m.project is None


def test_project_model():
    p = Project(metadata=Metadata(name="my-project"), spec=ProjectSpec())
    assert p.kind == "Project"
    assert p.metadata.name == "my-project"


def test_dashboard_model():
    d = Dashboard(
        metadata=Metadata(name="my-dash", project="my-project"),
        spec=DashboardSpec(),
    )
    assert d.kind == "Dashboard"


def test_user_model():
    u = User(
        metadata=Metadata(name="alice"),
        spec=UserSpec(native_provider={"password": "secret"}),
    )
    assert u.kind == "User"
    assert u.metadata.name == "alice"


def test_public_api_imports():
    from perses_api import (
        APIModel,
        Api,
        Project,
        Dashboard,
        EphemeralDashboard,
        ProjectDatasource,
        GlobalDatasource,
        ProjectVariable,
        GlobalVariable,
        ProjectRole,
        GlobalRole,
        ProjectRoleBinding,
        GlobalRoleBinding,
        ProjectSecret,
        GlobalSecret,
        User,
        Plugin,
        Migrate,
        Validate,
    )
    assert APIModel is not None
