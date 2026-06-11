from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class _CamelModel(BaseModel):
    """Base model that serialises to/from camelCase JSON matching the Perses API wire format."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


# ---------------------------------------------------------------------------
# Connection configuration
# ---------------------------------------------------------------------------


@dataclass
class APIModel:
    """The dataclass includes all necessary values and information to access the Perses API

    Args:
        host (str): Specify the host of the Perses instance
        token (str): Specify the bearer token for authentication (default None)
        username (str): Specify the username for basic authentication (default None)
        password (str): Specify the password for basic authentication (default None)
        timeout (float): Specify the timeout of the API call (default 10.0)
        headers (dict): Specify additional HTTP headers to include in every request (default None)
        http2_support (bool): Specify if HTTP/2 should be used (default False)
        ssl_context (any): Specify a custom SSL context or certificate path (default None)
        num_pools (int): Specify the maximum number of HTTP connections (default 10)
        retries (any): Specify the number of retries or a retry object (default False)
        follow_redirects (bool): Specify if HTTP redirects should be followed (default True)
    """

    host: str  #: The host of the Perses instance
    token: Optional[str] = None  #: Bearer token for authentication
    username: Optional[str] = None  #: Username for basic authentication
    password: Optional[str] = None  #: Password for basic authentication
    timeout: float = 10.0  #: Timeout of the API call in seconds
    headers: Optional[dict] = (
        None  #: Additional HTTP headers to include in every request
    )
    http2_support: bool = False  #: Whether to use HTTP/2
    ssl_context: Any = None  #: Custom SSL context or certificate path
    num_pools: int = 10  #: Maximum number of HTTP connections
    retries: Any = False  #: Number of retries or a retry object
    follow_redirects: bool = True  #: Whether to follow HTTP redirects


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class RequestsMethods(str, Enum):
    """The enum includes all necessary methods to access the Perses API"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class APIEndpoints(str, Enum):
    """The enum includes all necessary API endpoint path templates for the Perses API"""

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


class Metadata(_CamelModel):
    """The class includes the common metadata envelope shared by all Perses resources

    Args:
        name (str): Specify the name of the resource
        project (str): Specify the project the resource belongs to (default None)
        created_at (str): Specify the creation timestamp (default None)
        updated_at (str): Specify the last update timestamp (default None)
        version (int): Specify the resource version for optimistic concurrency (default None)
    """

    name: str
    project: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    version: Optional[int] = None


# ---------------------------------------------------------------------------
# Resource models
# ---------------------------------------------------------------------------


class ProjectSpec(_CamelModel):
    """The class includes the spec for a Perses project resource

    Args:
        display (dict): Specify optional display properties such as a human-readable name (default None)
    """

    display: Optional[dict] = None


class Project(_CamelModel):
    """The class includes all necessary values to represent a Perses project resource

    Args:
        kind (str): Specify the resource kind (default Project)
        metadata (Metadata): Specify the resource metadata
        spec (ProjectSpec): Specify the project spec (default ProjectSpec)
    """

    kind: str = "Project"
    metadata: Metadata
    spec: ProjectSpec = Field(default_factory=ProjectSpec)


class DashboardSpec(_CamelModel):
    """The class includes the spec for a Perses dashboard resource

    Args:
        display (dict): Specify optional display properties (default None)
        datasources (dict): Specify the datasource references used by the dashboard (default None)
        variables (list): Specify the dashboard-scoped variables (default None)
        panels (dict): Specify the panel definitions keyed by panel ID (default None)
        layouts (list): Specify the layout configuration for the panels (default None)
        duration (str): Specify the default time range duration, e.g. 1h (default None)
        refresh_interval (str): Specify the default auto-refresh interval, e.g. 30s (default None)
    """

    display: Optional[dict] = None
    datasources: Optional[dict] = None
    variables: Optional[list] = None
    panels: Optional[dict] = None
    layouts: Optional[list] = None
    duration: Optional[str] = None
    refresh_interval: Optional[str] = None


class Dashboard(_CamelModel):
    """The class includes all necessary values to represent a Perses dashboard resource

    Args:
        kind (str): Specify the resource kind (default Dashboard)
        metadata (Metadata): Specify the resource metadata
        spec (DashboardSpec): Specify the dashboard spec (default DashboardSpec)
    """

    kind: str = "Dashboard"
    metadata: Metadata
    spec: DashboardSpec = Field(default_factory=DashboardSpec)


class EphemeralDashboardSpec(_CamelModel):
    """The class includes the spec for a Perses ephemeral dashboard resource

    Args:
        ttl (str): Specify the time-to-live duration after which the dashboard is deleted, e.g. 1h
        display (dict): Specify optional display properties (default None)
        datasources (dict): Specify the datasource references used by the dashboard (default None)
        variables (list): Specify the dashboard-scoped variables (default None)
        panels (dict): Specify the panel definitions keyed by panel ID (default None)
        layouts (list): Specify the layout configuration for the panels (default None)
        duration (str): Specify the default time range duration (default None)
        refresh_interval (str): Specify the default auto-refresh interval (default None)
    """

    ttl: str
    display: Optional[dict] = None
    datasources: Optional[dict] = None
    variables: Optional[list] = None
    panels: Optional[dict] = None
    layouts: Optional[list] = None
    duration: Optional[str] = None
    refresh_interval: Optional[str] = None


class EphemeralDashboard(_CamelModel):
    """The class includes all necessary values to represent a Perses ephemeral dashboard resource

    Args:
        kind (str): Specify the resource kind (default EphemeralDashboard)
        metadata (Metadata): Specify the resource metadata
        spec (EphemeralDashboardSpec): Specify the ephemeral dashboard spec including TTL
    """

    kind: str = "EphemeralDashboard"
    metadata: Metadata
    spec: EphemeralDashboardSpec


class DatasourceSpec(_CamelModel):
    """The class includes the spec for a Perses datasource resource

    Args:
        default (bool): Specify if this datasource is the default for its type (default False)
        plugin (dict): Specify the plugin configuration including kind and plugin-specific spec (default {})
    """

    default: bool = False
    plugin: dict = Field(default_factory=dict)


class Datasource(_CamelModel):
    """The class includes all necessary values to represent a project-scoped Perses datasource resource

    Args:
        kind (str): Specify the resource kind (default Datasource)
        metadata (Metadata): Specify the resource metadata including project
        spec (DatasourceSpec): Specify the datasource spec
    """

    kind: str = "Datasource"
    metadata: Metadata
    spec: DatasourceSpec


class GlobalDatasource(_CamelModel):
    """The class includes all necessary values to represent a global Perses datasource resource

    Args:
        kind (str): Specify the resource kind (default GlobalDatasource)
        metadata (Metadata): Specify the resource metadata
        spec (DatasourceSpec): Specify the datasource spec
    """

    kind: str = "GlobalDatasource"
    metadata: Metadata
    spec: DatasourceSpec


class VariableSpec(_CamelModel):
    """The class includes the spec for a Perses variable resource

    Args:
        kind (str): Specify the variable kind, e.g. StaticListVariable or QueryVariable
        spec (dict): Specify the variable kind-specific configuration (default {})
    """

    kind: str
    spec: dict = Field(default_factory=dict)


class Variable(_CamelModel):
    """The class includes all necessary values to represent a project-scoped Perses variable resource

    Args:
        kind (str): Specify the resource kind (default Variable)
        metadata (Metadata): Specify the resource metadata including project
        spec (VariableSpec): Specify the variable spec
    """

    kind: str = "Variable"
    metadata: Metadata
    spec: VariableSpec


class GlobalVariable(_CamelModel):
    """The class includes all necessary values to represent a global Perses variable resource

    Args:
        kind (str): Specify the resource kind (default GlobalVariable)
        metadata (Metadata): Specify the resource metadata
        spec (VariableSpec): Specify the variable spec
    """

    kind: str = "GlobalVariable"
    metadata: Metadata
    spec: VariableSpec


class Permission(_CamelModel):
    """The class includes a single permission entry for a Perses role

    Args:
        actions (list[str]): Specify the allowed actions, e.g. read, write, or * for all
        scopes (list[str]): Specify the resource scopes the actions apply to, e.g. Dashboard or *
    """

    actions: list[str]
    scopes: list[str]


class RoleSpec(_CamelModel):
    """The class includes the spec for a Perses role resource

    Args:
        permissions (list[Permission]): Specify the list of permissions granted by the role (default [])
    """

    permissions: list[Permission] = Field(default_factory=list)


class Role(_CamelModel):
    """The class includes all necessary values to represent a project-scoped Perses role resource

    Args:
        kind (str): Specify the resource kind (default Role)
        metadata (Metadata): Specify the resource metadata including project
        spec (RoleSpec): Specify the role spec (default RoleSpec)
    """

    kind: str = "Role"
    metadata: Metadata
    spec: RoleSpec = Field(default_factory=RoleSpec)


class GlobalRole(_CamelModel):
    """The class includes all necessary values to represent a global Perses role resource

    Args:
        kind (str): Specify the resource kind (default GlobalRole)
        metadata (Metadata): Specify the resource metadata
        spec (RoleSpec): Specify the role spec (default RoleSpec)
    """

    kind: str = "GlobalRole"
    metadata: Metadata
    spec: RoleSpec = Field(default_factory=RoleSpec)


class Subject(_CamelModel):
    """The class includes a single subject entry for a Perses role binding

    Args:
        kind (str): Specify the subject kind, e.g. User or Team
        name (str): Specify the name of the subject
    """

    kind: str
    name: str


class RoleBindingSpec(_CamelModel):
    """The class includes the spec for a Perses role binding resource

    Args:
        role (str): Specify the name of the role to bind
        subjects (list[Subject]): Specify the subjects the role is bound to (default [])
    """

    role: str
    subjects: list[Subject] = Field(default_factory=list)


class RoleBinding(_CamelModel):
    """The class includes all necessary values to represent a project-scoped Perses role binding resource

    Args:
        kind (str): Specify the resource kind (default RoleBinding)
        metadata (Metadata): Specify the resource metadata including project
        spec (RoleBindingSpec): Specify the role binding spec
    """

    kind: str = "RoleBinding"
    metadata: Metadata
    spec: RoleBindingSpec


class GlobalRoleBinding(_CamelModel):
    """The class includes all necessary values to represent a global Perses role binding resource

    Args:
        kind (str): Specify the resource kind (default GlobalRoleBinding)
        metadata (Metadata): Specify the resource metadata
        spec (RoleBindingSpec): Specify the role binding spec
    """

    kind: str = "GlobalRoleBinding"
    metadata: Metadata
    spec: RoleBindingSpec


class SecretSpec(_CamelModel):
    """The class includes the spec for a Perses secret resource

    Args:
        kind (str): Specify the secret kind, e.g. BasicAuth or BearerToken
        spec (dict): Specify the secret kind-specific configuration (default {})
    """

    kind: str
    spec: dict = Field(default_factory=dict)


class Secret(_CamelModel):
    """The class includes all necessary values to represent a project-scoped Perses secret resource

    Args:
        kind (str): Specify the resource kind (default Secret)
        metadata (Metadata): Specify the resource metadata including project
        spec (SecretSpec): Specify the secret spec
    """

    kind: str = "Secret"
    metadata: Metadata
    spec: SecretSpec


class GlobalSecret(_CamelModel):
    """The class includes all necessary values to represent a global Perses secret resource

    Args:
        kind (str): Specify the resource kind (default GlobalSecret)
        metadata (Metadata): Specify the resource metadata
        spec (SecretSpec): Specify the secret spec
    """

    kind: str = "GlobalSecret"
    metadata: Metadata
    spec: SecretSpec


class UserSpec(_CamelModel):
    """The class includes the spec for a Perses user resource

    Args:
        first_name (str): Specify the user's first name (default None)
        last_name (str): Specify the user's last name (default None)
        native_provider (dict): Specify the native authentication provider config including password (default None)
        oauth_providers (list): Specify the list of OAuth provider configurations (default None)
    """

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    native_provider: Optional[dict] = None
    oauth_providers: Optional[list] = None


class User(_CamelModel):
    """The class includes all necessary values to represent a Perses user resource

    Args:
        kind (str): Specify the resource kind (default User)
        metadata (Metadata): Specify the resource metadata
        spec (UserSpec): Specify the user spec (default UserSpec)
    """

    kind: str = "User"
    metadata: Metadata
    spec: UserSpec = Field(default_factory=UserSpec)


class PluginMetadata(_CamelModel):
    """The class includes the metadata for a Perses plugin module

    Args:
        name (str): Specify the plugin module name
        version (str): Specify the plugin module version
    """

    name: str
    version: str


class PluginEntry(_CamelModel):
    """The class includes a single plugin entry within a plugin module

    Args:
        kind (str): Specify the plugin kind
        display (dict): Specify optional display properties for the plugin (default None)
    """

    kind: str
    display: Optional[dict] = None


class PluginModuleSpec(_CamelModel):
    """The class includes the spec for a Perses plugin module resource

    Args:
        schemas_path (str): Specify the path to the plugin schemas directory (default None)
        plugins (list[PluginEntry]): Specify the list of plugins provided by this module (default [])
    """

    schemas_path: Optional[str] = None
    plugins: list[PluginEntry] = Field(default_factory=list)


class PluginModule(_CamelModel):
    """The class includes all necessary values to represent a Perses plugin module resource

    Args:
        kind (str): Specify the resource kind (default PluginModule)
        metadata (PluginMetadata): Specify the plugin module metadata including name and version
        spec (PluginModuleSpec): Specify the plugin module spec (default PluginModuleSpec)
    """

    kind: str = "PluginModule"
    metadata: PluginMetadata
    spec: PluginModuleSpec = Field(default_factory=PluginModuleSpec)
