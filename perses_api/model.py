from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Connection configuration
# ---------------------------------------------------------------------------

@dataclass
class APIModel:
    host: str
    token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    timeout: float = 10.0
    headers: Optional[dict] = None
    http2_support: bool = False
    ssl_context: Any = None
    num_pools: int = 10
    retries: Any = False
    follow_redirects: bool = True


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RequestsMethods(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class APIEndpoints(str, Enum):
    PROJECTS = "/api/v1/projects"
    PROJECT = "/api/v1/projects/{project}"
    DASHBOARDS = "/api/v1/projects/{project}/dashboards"
    DASHBOARD = "/api/v1/projects/{project}/dashboards/{name}"
    EPHEMERAL_DASHBOARDS = "/api/v1/projects/{project}/ephemeraldashboards"
    EPHEMERAL_DASHBOARD = "/api/v1/projects/{project}/ephemeraldashboards/{name}"
    DATASOURCES = "/api/v1/projects/{project}/datasources"
    DATASOURCE = "/api/v1/projects/{project}/datasources/{name}"
    GLOBAL_DATASOURCES = "/api/v1/globaldatasources"
    GLOBAL_DATASOURCE = "/api/v1/globaldatasources/{name}"
    VARIABLES = "/api/v1/projects/{project}/variables"
    VARIABLE = "/api/v1/projects/{project}/variables/{name}"
    GLOBAL_VARIABLES = "/api/v1/globalvariables"
    GLOBAL_VARIABLE = "/api/v1/globalvariables/{name}"
    ROLES = "/api/v1/projects/{project}/roles"
    ROLE = "/api/v1/projects/{project}/roles/{name}"
    GLOBAL_ROLES = "/api/v1/globalroles"
    GLOBAL_ROLE = "/api/v1/globalroles/{name}"
    ROLE_BINDINGS = "/api/v1/projects/{project}/rolebindings"
    ROLE_BINDING = "/api/v1/projects/{project}/rolebindings/{name}"
    GLOBAL_ROLE_BINDINGS = "/api/v1/globalrolebindings"
    GLOBAL_ROLE_BINDING = "/api/v1/globalrolebindings/{name}"
    SECRETS = "/api/v1/projects/{project}/secrets"
    SECRET = "/api/v1/projects/{project}/secrets/{name}"
    GLOBAL_SECRETS = "/api/v1/globalsecrets"
    GLOBAL_SECRET = "/api/v1/globalsecrets/{name}"
    USERS = "/api/v1/users"
    USER = "/api/v1/users/{name}"
    PLUGINS = "/api/v1/plugins"
    MIGRATE = "/api/migrate"
    VALIDATE = "/api/validate/{resource_type}"


# ---------------------------------------------------------------------------
# Shared envelope
# ---------------------------------------------------------------------------

class Metadata(BaseModel):
    name: str
    project: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    version: Optional[int] = None


# ---------------------------------------------------------------------------
# Resource models
# ---------------------------------------------------------------------------

class ProjectSpec(BaseModel):
    display: Optional[dict] = None


class Project(BaseModel):
    kind: str = "Project"
    metadata: Metadata
    spec: ProjectSpec = Field(default_factory=ProjectSpec)


class DashboardSpec(BaseModel):
    display: Optional[dict] = None
    datasources: Optional[dict] = None
    variables: Optional[list] = None
    panels: Optional[dict] = None
    layouts: Optional[list] = None
    duration: Optional[str] = None
    refresh_interval: Optional[str] = None


class Dashboard(BaseModel):
    kind: str = "Dashboard"
    metadata: Metadata
    spec: DashboardSpec = Field(default_factory=DashboardSpec)


class EphemeralDashboardSpec(BaseModel):
    ttl: str
    display: Optional[dict] = None
    datasources: Optional[dict] = None
    variables: Optional[list] = None
    panels: Optional[dict] = None
    layouts: Optional[list] = None
    duration: Optional[str] = None
    refresh_interval: Optional[str] = None


class EphemeralDashboard(BaseModel):
    kind: str = "EphemeralDashboard"
    metadata: Metadata
    spec: EphemeralDashboardSpec


class DatasourceSpec(BaseModel):
    default: bool = False
    plugin: dict = Field(default_factory=dict)


class Datasource(BaseModel):
    kind: str = "Datasource"
    metadata: Metadata
    spec: DatasourceSpec


class GlobalDatasource(BaseModel):
    kind: str = "GlobalDatasource"
    metadata: Metadata
    spec: DatasourceSpec


class VariableSpec(BaseModel):
    kind: str
    spec: dict = Field(default_factory=dict)


class Variable(BaseModel):
    kind: str = "Variable"
    metadata: Metadata
    spec: VariableSpec


class GlobalVariable(BaseModel):
    kind: str = "GlobalVariable"
    metadata: Metadata
    spec: VariableSpec


class Permission(BaseModel):
    actions: list[str]
    scopes: list[str]


class RoleSpec(BaseModel):
    permissions: list[Permission] = Field(default_factory=list)


class Role(BaseModel):
    kind: str = "Role"
    metadata: Metadata
    spec: RoleSpec = Field(default_factory=RoleSpec)


class GlobalRole(BaseModel):
    kind: str = "GlobalRole"
    metadata: Metadata
    spec: RoleSpec = Field(default_factory=RoleSpec)


class Subject(BaseModel):
    kind: str
    name: str


class RoleBindingSpec(BaseModel):
    role: str
    subjects: list[Subject] = Field(default_factory=list)


class RoleBinding(BaseModel):
    kind: str = "RoleBinding"
    metadata: Metadata
    spec: RoleBindingSpec


class GlobalRoleBinding(BaseModel):
    kind: str = "GlobalRoleBinding"
    metadata: Metadata
    spec: RoleBindingSpec


class SecretSpec(BaseModel):
    kind: str
    spec: dict = Field(default_factory=dict)


class Secret(BaseModel):
    kind: str = "Secret"
    metadata: Metadata
    spec: SecretSpec


class GlobalSecret(BaseModel):
    kind: str = "GlobalSecret"
    metadata: Metadata
    spec: SecretSpec


class UserSpec(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    native_provider: Optional[dict] = None
    oauth_providers: Optional[list] = None


class User(BaseModel):
    kind: str = "User"
    metadata: Metadata
    spec: UserSpec = Field(default_factory=UserSpec)


class PluginMetadata(BaseModel):
    name: str
    version: str


class PluginEntry(BaseModel):
    kind: str
    display: Optional[dict] = None


class PluginModuleSpec(BaseModel):
    schemas_path: Optional[str] = None
    plugins: list[PluginEntry] = Field(default_factory=list)


class PluginModule(BaseModel):
    kind: str = "PluginModule"
    metadata: PluginMetadata
    spec: PluginModuleSpec = Field(default_factory=PluginModuleSpec)
