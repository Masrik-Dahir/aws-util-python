"""Native async ECS utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.ecs import (
    CreateCapacityProviderResult,
    CreateClusterResult,
    CreateServiceResult,
    CreateTaskSetResult,
    DeleteAccountSettingResult,
    DeleteAttributesResult,
    DeleteCapacityProviderResult,
    DeleteClusterResult,
    DeleteServiceResult,
    DeleteTaskDefinitionsResult,
    DeleteTaskSetResult,
    DeregisterContainerInstanceResult,
    DeregisterTaskDefinitionResult,
    DescribeCapacityProvidersResult,
    DescribeClustersResult,
    DescribeContainerInstancesResult,
    DescribeServiceDeploymentsResult,
    DescribeServiceRevisionsResult,
    DescribeTaskSetsResult,
    DiscoverPollEndpointResult,
    ECSService,
    ECSTask,
    ECSTaskDefinition,
    ExecuteCommandResult,
    GetTaskProtectionResult,
    ListAccountSettingsResult,
    ListAttributesResult,
    ListContainerInstancesResult,
    ListServiceDeploymentsResult,
    ListServicesByNamespaceResult,
    ListServicesResult,
    ListTagsForResourceResult,
    ListTaskDefinitionFamiliesResult,
    ListTaskDefinitionsResult,
    PutAccountSettingDefaultResult,
    PutAccountSettingResult,
    PutAttributesResult,
    PutClusterCapacityProvidersResult,
    RegisterContainerInstanceResult,
    RegisterTaskDefinitionResult,
    StartTaskResult,
    StopServiceDeploymentResult,
    SubmitAttachmentStateChangesResult,
    SubmitContainerStateChangeResult,
    SubmitTaskStateChangeResult,
    UpdateCapacityProviderResult,
    UpdateClusterResult,
    UpdateClusterSettingsResult,
    UpdateContainerAgentResult,
    UpdateContainerInstancesStateResult,
    UpdateServicePrimaryTaskSetResult,
    UpdateTaskProtectionResult,
    UpdateTaskSetResult,
    _parse_task,
)
from aws_util.exceptions import AwsServiceError, wrap_aws_error

__all__ = [
    "CreateCapacityProviderResult",
    "CreateClusterResult",
    "CreateServiceResult",
    "CreateTaskSetResult",
    "DeleteAccountSettingResult",
    "DeleteAttributesResult",
    "DeleteCapacityProviderResult",
    "DeleteClusterResult",
    "DeleteServiceResult",
    "DeleteTaskDefinitionsResult",
    "DeleteTaskSetResult",
    "DeregisterContainerInstanceResult",
    "DeregisterTaskDefinitionResult",
    "DescribeCapacityProvidersResult",
    "DescribeClustersResult",
    "DescribeContainerInstancesResult",
    "DescribeServiceDeploymentsResult",
    "DescribeServiceRevisionsResult",
    "DescribeTaskSetsResult",
    "DiscoverPollEndpointResult",
    "ECSService",
    "ECSTask",
    "ECSTaskDefinition",
    "ExecuteCommandResult",
    "GetTaskProtectionResult",
    "ListAccountSettingsResult",
    "ListAttributesResult",
    "ListContainerInstancesResult",
    "ListServiceDeploymentsResult",
    "ListServicesByNamespaceResult",
    "ListServicesResult",
    "ListTagsForResourceResult",
    "ListTaskDefinitionFamiliesResult",
    "ListTaskDefinitionsResult",
    "PutAccountSettingDefaultResult",
    "PutAccountSettingResult",
    "PutAttributesResult",
    "PutClusterCapacityProvidersResult",
    "RegisterContainerInstanceResult",
    "RegisterTaskDefinitionResult",
    "StartTaskResult",
    "StopServiceDeploymentResult",
    "SubmitAttachmentStateChangesResult",
    "SubmitContainerStateChangeResult",
    "SubmitTaskStateChangeResult",
    "UpdateCapacityProviderResult",
    "UpdateClusterResult",
    "UpdateClusterSettingsResult",
    "UpdateContainerAgentResult",
    "UpdateContainerInstancesStateResult",
    "UpdateServicePrimaryTaskSetResult",
    "UpdateTaskProtectionResult",
    "UpdateTaskSetResult",
    "create_capacity_provider",
    "create_cluster",
    "create_service",
    "create_task_set",
    "delete_account_setting",
    "delete_attributes",
    "delete_capacity_provider",
    "delete_cluster",
    "delete_service",
    "delete_task_definitions",
    "delete_task_set",
    "deregister_container_instance",
    "deregister_task_definition",
    "describe_capacity_providers",
    "describe_clusters",
    "describe_container_instances",
    "describe_service_deployments",
    "describe_service_revisions",
    "describe_services",
    "describe_task_definition",
    "describe_task_sets",
    "describe_tasks",
    "discover_poll_endpoint",
    "execute_command",
    "get_task_protection",
    "list_account_settings",
    "list_attributes",
    "list_clusters",
    "list_container_instances",
    "list_service_deployments",
    "list_services",
    "list_services_by_namespace",
    "list_tags_for_resource",
    "list_task_definition_families",
    "list_task_definitions",
    "list_tasks",
    "put_account_setting",
    "put_account_setting_default",
    "put_attributes",
    "put_cluster_capacity_providers",
    "register_container_instance",
    "register_task_definition",
    "run_task",
    "run_task_and_wait",
    "start_task",
    "stop_service_deployment",
    "stop_task",
    "submit_attachment_state_changes",
    "submit_container_state_change",
    "submit_task_state_change",
    "tag_resource",
    "untag_resource",
    "update_capacity_provider",
    "update_cluster",
    "update_cluster_settings",
    "update_container_agent",
    "update_container_instances_state",
    "update_service",
    "update_service_primary_task_set",
    "update_task_protection",
    "update_task_set",
    "wait_for_service_stable",
    "wait_for_task",
]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def list_clusters(
    region_name: str | None = None,
) -> list[str]:
    """List all ECS cluster ARNs in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of cluster ARNs.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    try:
        items = await client.paginate("ListClusters", "clusterArns")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_clusters failed") from exc
    return [str(item) for item in items]


async def run_task(
    cluster: str,
    task_definition: str,
    launch_type: str = "FARGATE",
    subnets: list[str] | None = None,
    security_groups: list[str] | None = None,
    assign_public_ip: str = "DISABLED",
    overrides: dict[str, Any] | None = None,
    count: int = 1,
    region_name: str | None = None,
) -> list[ECSTask]:
    """Run one or more ECS tasks.

    Args:
        cluster: Cluster name or ARN.
        task_definition: Task definition family:revision or ARN.
        launch_type: ``"FARGATE"`` (default) or ``"EC2"``.
        subnets: VPC subnet IDs for Fargate tasks.
        security_groups: Security group IDs for Fargate tasks.
        assign_public_ip: ``"ENABLED"`` or ``"DISABLED"`` (default).
        overrides: Optional container overrides dict passed to boto3.
        count: Number of tasks to run.
        region_name: AWS region override.

    Returns:
        A list of :class:`ECSTask` objects for the launched tasks.

    Raises:
        RuntimeError: If the run request fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {
        "cluster": cluster,
        "taskDefinition": task_definition,
        "launchType": launch_type,
        "count": count,
    }
    if subnets or security_groups:
        kwargs["networkConfiguration"] = {
            "awsvpcConfiguration": {
                "subnets": subnets or [],
                "securityGroups": security_groups or [],
                "assignPublicIp": assign_public_ip,
            }
        }
    if overrides:
        kwargs["overrides"] = overrides

    try:
        resp = await client.call("RunTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"run_task failed on cluster {cluster!r}") from exc

    if resp.get("failures"):
        raise AwsServiceError(f"ECS run_task failures: {resp['failures']}")
    return [_parse_task(t) for t in resp.get("tasks", [])]


async def stop_task(
    cluster: str,
    task_arn: str,
    reason: str = "",
    region_name: str | None = None,
) -> None:
    """Stop a running ECS task.

    Args:
        cluster: Cluster name or ARN.
        task_arn: ARN of the task to stop.
        reason: Human-readable reason for stopping (appears in task events).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the stop request fails.
    """
    client = async_client("ecs", region_name)
    try:
        await client.call("StopTask", cluster=cluster, task=task_arn, reason=reason)
    except Exception as exc:
        raise wrap_aws_error(exc, f"stop_task failed for {task_arn!r}") from exc


async def describe_tasks(
    cluster: str,
    task_arns: list[str],
    region_name: str | None = None,
) -> list[ECSTask]:
    """Describe one or more ECS tasks.

    Args:
        cluster: Cluster name or ARN.
        task_arns: Task ARNs or short IDs (up to 100).
        region_name: AWS region override.

    Returns:
        A list of :class:`ECSTask` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    try:
        resp = await client.call("DescribeTasks", cluster=cluster, tasks=task_arns)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_tasks failed") from exc
    return [_parse_task(t) for t in resp.get("tasks", [])]


async def list_tasks(
    cluster: str,
    service_name: str | None = None,
    desired_status: str = "RUNNING",
    region_name: str | None = None,
) -> list[str]:
    """List task ARNs in a cluster, optionally filtered by service.

    Args:
        cluster: Cluster name or ARN.
        service_name: Filter to tasks belonging to a specific service.
        desired_status: ``"RUNNING"`` (default), ``"PENDING"``, or
            ``"STOPPED"``.
        region_name: AWS region override.

    Returns:
        A list of task ARNs.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {
        "cluster": cluster,
        "desiredStatus": desired_status,
    }
    if service_name:
        kwargs["serviceName"] = service_name

    try:
        items = await client.paginate("ListTasks", "taskArns", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_tasks failed") from exc
    return [str(item) for item in items]


async def describe_services(
    cluster: str,
    service_names: list[str],
    region_name: str | None = None,
) -> list[ECSService]:
    """Describe one or more ECS services in a cluster.

    Args:
        cluster: Cluster name or ARN.
        service_names: Service names or ARNs (up to 10).
        region_name: AWS region override.

    Returns:
        A list of :class:`ECSService` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    try:
        resp = await client.call(
            "DescribeServices",
            cluster=cluster,
            services=service_names,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_services failed") from exc
    return [
        ECSService(
            service_arn=svc["serviceArn"],
            service_name=svc["serviceName"],
            cluster_arn=svc["clusterArn"],
            status=svc["status"],
            desired_count=svc["desiredCount"],
            running_count=svc["runningCount"],
            pending_count=svc["pendingCount"],
            task_definition=svc["taskDefinition"],
            launch_type=svc.get("launchType"),
        )
        for svc in resp.get("services", [])
    ]


async def update_service(
    cluster: str,
    service_name: str,
    desired_count: int | None = None,
    task_definition: str | None = None,
    force_new_deployment: bool = False,
    region_name: str | None = None,
) -> ECSService:
    """Update an ECS service (scale or deploy a new task definition).

    Args:
        cluster: Cluster name or ARN.
        service_name: Service name or ARN.
        desired_count: New desired task count.  ``None`` keeps the current
            value.
        task_definition: New task definition family:revision or ARN.
        force_new_deployment: Force a new deployment even if nothing changed.
        region_name: AWS region override.

    Returns:
        The updated :class:`ECSService`.

    Raises:
        RuntimeError: If the update fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {
        "cluster": cluster,
        "service": service_name,
        "forceNewDeployment": force_new_deployment,
    }
    if desired_count is not None:
        kwargs["desiredCount"] = desired_count
    if task_definition is not None:
        kwargs["taskDefinition"] = task_definition

    try:
        resp = await client.call("UpdateService", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_service failed for {service_name!r}") from exc
    svc = resp["service"]
    return ECSService(
        service_arn=svc["serviceArn"],
        service_name=svc["serviceName"],
        cluster_arn=svc["clusterArn"],
        status=svc["status"],
        desired_count=svc["desiredCount"],
        running_count=svc["runningCount"],
        pending_count=svc["pendingCount"],
        task_definition=svc["taskDefinition"],
        launch_type=svc.get("launchType"),
    )


async def describe_task_definition(
    task_definition: str,
    region_name: str | None = None,
) -> ECSTaskDefinition:
    """Describe an ECS task definition.

    Args:
        task_definition: Family:revision or ARN.
        region_name: AWS region override.

    Returns:
        An :class:`ECSTaskDefinition`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    try:
        resp = await client.call("DescribeTaskDefinition", taskDefinition=task_definition)
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"describe_task_definition failed for {task_definition!r}"
        ) from exc
    td = resp["taskDefinition"]
    return ECSTaskDefinition(
        task_definition_arn=td["taskDefinitionArn"],
        family=td["family"],
        revision=td["revision"],
        status=td["status"],
        cpu=td.get("cpu"),
        memory=td.get("memory"),
    )


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def wait_for_task(
    cluster: str,
    task_arn: str,
    target_status: str = "STOPPED",
    timeout: float = 600.0,
    poll_interval: float = 10.0,
    region_name: str | None = None,
) -> ECSTask:
    """Poll until an ECS task reaches a desired status.

    Args:
        cluster: Cluster name or ARN.
        task_arn: Task ARN to monitor.
        target_status: Status to wait for (default ``"STOPPED"``).
        timeout: Maximum seconds to wait (default ``600``).
        poll_interval: Seconds between checks (default ``10``).
        region_name: AWS region override.

    Returns:
        The :class:`ECSTask` in the target status.

    Raises:
        TimeoutError: If the task does not reach the target status in time.
        RuntimeError: If the task is not found.
    """
    import time as _time

    deadline = _time.monotonic() + timeout
    while True:
        tasks = await describe_tasks(cluster, [task_arn], region_name=region_name)
        if not tasks:
            raise AwsServiceError(f"Task {task_arn!r} not found in cluster {cluster!r}")
        task = tasks[0]
        if task.last_status == target_status:
            return task
        if _time.monotonic() >= deadline:
            raise TimeoutError(
                f"Task {task_arn!r} did not reach status "
                f"{target_status!r} within {timeout}s "
                f"(current: {task.last_status!r})"
            )
        await asyncio.sleep(poll_interval)


async def run_task_and_wait(
    cluster: str,
    task_definition: str,
    timeout: float = 600.0,
    launch_type: str = "FARGATE",
    subnets: list[str] | None = None,
    security_groups: list[str] | None = None,
    overrides: dict | None = None,
    region_name: str | None = None,
) -> ECSTask:
    """Run a single ECS task and wait until it stops.

    Combines :func:`run_task` and :func:`wait_for_task`.

    Args:
        cluster: Cluster name or ARN.
        task_definition: Task definition family:revision or ARN.
        timeout: Maximum seconds to wait for the task to stop.
        launch_type: ``"FARGATE"`` (default) or ``"EC2"``.
        subnets: VPC subnet IDs.
        security_groups: Security group IDs.
        overrides: Optional container overrides.
        region_name: AWS region override.

    Returns:
        The final :class:`ECSTask` (``last_status == "STOPPED"``).

    Raises:
        TimeoutError: If the task does not stop within *timeout*.
        RuntimeError: If the run or describe calls fail.
    """
    tasks = await run_task(
        cluster,
        task_definition,
        launch_type=launch_type,
        subnets=subnets,
        security_groups=security_groups,
        overrides=overrides,
        count=1,
        region_name=region_name,
    )
    return await wait_for_task(
        cluster,
        tasks[0].task_arn,
        timeout=timeout,
        region_name=region_name,
    )


async def wait_for_service_stable(
    cluster: str,
    service_name: str,
    timeout: float = 600.0,
    poll_interval: float = 15.0,
    region_name: str | None = None,
) -> ECSService:
    """Wait until an ECS service has all desired tasks running and healthy.

    Considers the service stable when ``running_count == desired_count`` and
    ``pending_count == 0``.

    Args:
        cluster: Cluster name or ARN.
        service_name: Service name or ARN.
        timeout: Maximum seconds to wait (default ``600``).
        poll_interval: Seconds between checks (default ``15``).
        region_name: AWS region override.

    Returns:
        The stable :class:`ECSService`.

    Raises:
        TimeoutError: If the service does not stabilise within *timeout*.
        RuntimeError: If the service is not found.
    """
    import time as _time

    deadline = _time.monotonic() + timeout
    while True:
        services = await describe_services(cluster, [service_name], region_name=region_name)
        if not services:
            raise AwsServiceError(f"Service {service_name!r} not found in cluster {cluster!r}")
        svc = services[0]
        if svc.running_count == svc.desired_count and svc.pending_count == 0:
            return svc
        if _time.monotonic() >= deadline:
            raise TimeoutError(
                f"Service {service_name!r} did not stabilise within "
                f"{timeout}s (running={svc.running_count}, "
                f"desired={svc.desired_count}, "
                f"pending={svc.pending_count})"
            )
        await asyncio.sleep(poll_interval)


async def create_capacity_provider(
    name: str,
    *,
    cluster: str | None = None,
    auto_scaling_group_provider: dict[str, Any] | None = None,
    managed_instances_provider: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCapacityProviderResult:
    """Create capacity provider.

    Args:
        name: Name.
        cluster: Cluster.
        auto_scaling_group_provider: Auto scaling group provider.
        managed_instances_provider: Managed instances provider.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if cluster is not None:
        kwargs["cluster"] = cluster
    if auto_scaling_group_provider is not None:
        kwargs["autoScalingGroupProvider"] = auto_scaling_group_provider
    if managed_instances_provider is not None:
        kwargs["managedInstancesProvider"] = managed_instances_provider
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateCapacityProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create capacity provider") from exc
    return CreateCapacityProviderResult(
        capacity_provider=resp.get("capacityProvider"),
    )


async def create_cluster(
    *,
    cluster_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    settings: list[dict[str, Any]] | None = None,
    configuration: dict[str, Any] | None = None,
    capacity_providers: list[str] | None = None,
    default_capacity_provider_strategy: list[dict[str, Any]] | None = None,
    service_connect_defaults: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateClusterResult:
    """Create cluster.

    Args:
        cluster_name: Cluster name.
        tags: Tags.
        settings: Settings.
        configuration: Configuration.
        capacity_providers: Capacity providers.
        default_capacity_provider_strategy: Default capacity provider strategy.
        service_connect_defaults: Service connect defaults.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_name is not None:
        kwargs["clusterName"] = cluster_name
    if tags is not None:
        kwargs["tags"] = tags
    if settings is not None:
        kwargs["settings"] = settings
    if configuration is not None:
        kwargs["configuration"] = configuration
    if capacity_providers is not None:
        kwargs["capacityProviders"] = capacity_providers
    if default_capacity_provider_strategy is not None:
        kwargs["defaultCapacityProviderStrategy"] = default_capacity_provider_strategy
    if service_connect_defaults is not None:
        kwargs["serviceConnectDefaults"] = service_connect_defaults
    try:
        resp = await client.call("CreateCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create cluster") from exc
    return CreateClusterResult(
        cluster=resp.get("cluster"),
    )


async def create_service(
    service_name: str,
    *,
    cluster: str | None = None,
    task_definition: str | None = None,
    availability_zone_rebalancing: str | None = None,
    load_balancers: list[dict[str, Any]] | None = None,
    service_registries: list[dict[str, Any]] | None = None,
    desired_count: int | None = None,
    client_token: str | None = None,
    launch_type: str | None = None,
    capacity_provider_strategy: list[dict[str, Any]] | None = None,
    platform_version: str | None = None,
    role: str | None = None,
    deployment_configuration: dict[str, Any] | None = None,
    placement_constraints: list[dict[str, Any]] | None = None,
    placement_strategy: list[dict[str, Any]] | None = None,
    network_configuration: dict[str, Any] | None = None,
    health_check_grace_period_seconds: int | None = None,
    scheduling_strategy: str | None = None,
    deployment_controller: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    enable_ecs_managed_tags: bool | None = None,
    propagate_tags: str | None = None,
    enable_execute_command: bool | None = None,
    service_connect_configuration: dict[str, Any] | None = None,
    volume_configurations: list[dict[str, Any]] | None = None,
    vpc_lattice_configurations: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateServiceResult:
    """Create service.

    Args:
        service_name: Service name.
        cluster: Cluster.
        task_definition: Task definition.
        availability_zone_rebalancing: Availability zone rebalancing.
        load_balancers: Load balancers.
        service_registries: Service registries.
        desired_count: Desired count.
        client_token: Client token.
        launch_type: Launch type.
        capacity_provider_strategy: Capacity provider strategy.
        platform_version: Platform version.
        role: Role.
        deployment_configuration: Deployment configuration.
        placement_constraints: Placement constraints.
        placement_strategy: Placement strategy.
        network_configuration: Network configuration.
        health_check_grace_period_seconds: Health check grace period seconds.
        scheduling_strategy: Scheduling strategy.
        deployment_controller: Deployment controller.
        tags: Tags.
        enable_ecs_managed_tags: Enable ecs managed tags.
        propagate_tags: Propagate tags.
        enable_execute_command: Enable execute command.
        service_connect_configuration: Service connect configuration.
        volume_configurations: Volume configurations.
        vpc_lattice_configurations: Vpc lattice configurations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceName"] = service_name
    if cluster is not None:
        kwargs["cluster"] = cluster
    if task_definition is not None:
        kwargs["taskDefinition"] = task_definition
    if availability_zone_rebalancing is not None:
        kwargs["availabilityZoneRebalancing"] = availability_zone_rebalancing
    if load_balancers is not None:
        kwargs["loadBalancers"] = load_balancers
    if service_registries is not None:
        kwargs["serviceRegistries"] = service_registries
    if desired_count is not None:
        kwargs["desiredCount"] = desired_count
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if launch_type is not None:
        kwargs["launchType"] = launch_type
    if capacity_provider_strategy is not None:
        kwargs["capacityProviderStrategy"] = capacity_provider_strategy
    if platform_version is not None:
        kwargs["platformVersion"] = platform_version
    if role is not None:
        kwargs["role"] = role
    if deployment_configuration is not None:
        kwargs["deploymentConfiguration"] = deployment_configuration
    if placement_constraints is not None:
        kwargs["placementConstraints"] = placement_constraints
    if placement_strategy is not None:
        kwargs["placementStrategy"] = placement_strategy
    if network_configuration is not None:
        kwargs["networkConfiguration"] = network_configuration
    if health_check_grace_period_seconds is not None:
        kwargs["healthCheckGracePeriodSeconds"] = health_check_grace_period_seconds
    if scheduling_strategy is not None:
        kwargs["schedulingStrategy"] = scheduling_strategy
    if deployment_controller is not None:
        kwargs["deploymentController"] = deployment_controller
    if tags is not None:
        kwargs["tags"] = tags
    if enable_ecs_managed_tags is not None:
        kwargs["enableECSManagedTags"] = enable_ecs_managed_tags
    if propagate_tags is not None:
        kwargs["propagateTags"] = propagate_tags
    if enable_execute_command is not None:
        kwargs["enableExecuteCommand"] = enable_execute_command
    if service_connect_configuration is not None:
        kwargs["serviceConnectConfiguration"] = service_connect_configuration
    if volume_configurations is not None:
        kwargs["volumeConfigurations"] = volume_configurations
    if vpc_lattice_configurations is not None:
        kwargs["vpcLatticeConfigurations"] = vpc_lattice_configurations
    try:
        resp = await client.call("CreateService", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create service") from exc
    return CreateServiceResult(
        service=resp.get("service"),
    )


async def create_task_set(
    service: str,
    cluster: str,
    task_definition: str,
    *,
    external_id: str | None = None,
    network_configuration: dict[str, Any] | None = None,
    load_balancers: list[dict[str, Any]] | None = None,
    service_registries: list[dict[str, Any]] | None = None,
    launch_type: str | None = None,
    capacity_provider_strategy: list[dict[str, Any]] | None = None,
    platform_version: str | None = None,
    scale: dict[str, Any] | None = None,
    client_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateTaskSetResult:
    """Create task set.

    Args:
        service: Service.
        cluster: Cluster.
        task_definition: Task definition.
        external_id: External id.
        network_configuration: Network configuration.
        load_balancers: Load balancers.
        service_registries: Service registries.
        launch_type: Launch type.
        capacity_provider_strategy: Capacity provider strategy.
        platform_version: Platform version.
        scale: Scale.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["service"] = service
    kwargs["cluster"] = cluster
    kwargs["taskDefinition"] = task_definition
    if external_id is not None:
        kwargs["externalId"] = external_id
    if network_configuration is not None:
        kwargs["networkConfiguration"] = network_configuration
    if load_balancers is not None:
        kwargs["loadBalancers"] = load_balancers
    if service_registries is not None:
        kwargs["serviceRegistries"] = service_registries
    if launch_type is not None:
        kwargs["launchType"] = launch_type
    if capacity_provider_strategy is not None:
        kwargs["capacityProviderStrategy"] = capacity_provider_strategy
    if platform_version is not None:
        kwargs["platformVersion"] = platform_version
    if scale is not None:
        kwargs["scale"] = scale
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateTaskSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create task set") from exc
    return CreateTaskSetResult(
        task_set=resp.get("taskSet"),
    )


async def delete_account_setting(
    name: str,
    *,
    principal_arn: str | None = None,
    region_name: str | None = None,
) -> DeleteAccountSettingResult:
    """Delete account setting.

    Args:
        name: Name.
        principal_arn: Principal arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if principal_arn is not None:
        kwargs["principalArn"] = principal_arn
    try:
        resp = await client.call("DeleteAccountSetting", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete account setting") from exc
    return DeleteAccountSettingResult(
        setting=resp.get("setting"),
    )


async def delete_attributes(
    attributes: list[dict[str, Any]],
    *,
    cluster: str | None = None,
    region_name: str | None = None,
) -> DeleteAttributesResult:
    """Delete attributes.

    Args:
        attributes: Attributes.
        cluster: Cluster.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["attributes"] = attributes
    if cluster is not None:
        kwargs["cluster"] = cluster
    try:
        resp = await client.call("DeleteAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete attributes") from exc
    return DeleteAttributesResult(
        attributes=resp.get("attributes"),
    )


async def delete_capacity_provider(
    capacity_provider: str,
    *,
    cluster: str | None = None,
    region_name: str | None = None,
) -> DeleteCapacityProviderResult:
    """Delete capacity provider.

    Args:
        capacity_provider: Capacity provider.
        cluster: Cluster.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["capacityProvider"] = capacity_provider
    if cluster is not None:
        kwargs["cluster"] = cluster
    try:
        resp = await client.call("DeleteCapacityProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete capacity provider") from exc
    return DeleteCapacityProviderResult(
        capacity_provider=resp.get("capacityProvider"),
    )


async def delete_cluster(
    cluster: str,
    region_name: str | None = None,
) -> DeleteClusterResult:
    """Delete cluster.

    Args:
        cluster: Cluster.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["cluster"] = cluster
    try:
        resp = await client.call("DeleteCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete cluster") from exc
    return DeleteClusterResult(
        cluster=resp.get("cluster"),
    )


async def delete_service(
    service: str,
    *,
    cluster: str | None = None,
    force: bool | None = None,
    region_name: str | None = None,
) -> DeleteServiceResult:
    """Delete service.

    Args:
        service: Service.
        cluster: Cluster.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["service"] = service
    if cluster is not None:
        kwargs["cluster"] = cluster
    if force is not None:
        kwargs["force"] = force
    try:
        resp = await client.call("DeleteService", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete service") from exc
    return DeleteServiceResult(
        service=resp.get("service"),
    )


async def delete_task_definitions(
    task_definitions: list[str],
    region_name: str | None = None,
) -> DeleteTaskDefinitionsResult:
    """Delete task definitions.

    Args:
        task_definitions: Task definitions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskDefinitions"] = task_definitions
    try:
        resp = await client.call("DeleteTaskDefinitions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete task definitions") from exc
    return DeleteTaskDefinitionsResult(
        task_definitions=resp.get("taskDefinitions"),
        failures=resp.get("failures"),
    )


async def delete_task_set(
    cluster: str,
    service: str,
    task_set: str,
    *,
    force: bool | None = None,
    region_name: str | None = None,
) -> DeleteTaskSetResult:
    """Delete task set.

    Args:
        cluster: Cluster.
        service: Service.
        task_set: Task set.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["cluster"] = cluster
    kwargs["service"] = service
    kwargs["taskSet"] = task_set
    if force is not None:
        kwargs["force"] = force
    try:
        resp = await client.call("DeleteTaskSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete task set") from exc
    return DeleteTaskSetResult(
        task_set=resp.get("taskSet"),
    )


async def deregister_container_instance(
    container_instance: str,
    *,
    cluster: str | None = None,
    force: bool | None = None,
    region_name: str | None = None,
) -> DeregisterContainerInstanceResult:
    """Deregister container instance.

    Args:
        container_instance: Container instance.
        cluster: Cluster.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["containerInstance"] = container_instance
    if cluster is not None:
        kwargs["cluster"] = cluster
    if force is not None:
        kwargs["force"] = force
    try:
        resp = await client.call("DeregisterContainerInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deregister container instance") from exc
    return DeregisterContainerInstanceResult(
        container_instance=resp.get("containerInstance"),
    )


async def deregister_task_definition(
    task_definition: str,
    region_name: str | None = None,
) -> DeregisterTaskDefinitionResult:
    """Deregister task definition.

    Args:
        task_definition: Task definition.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskDefinition"] = task_definition
    try:
        resp = await client.call("DeregisterTaskDefinition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deregister task definition") from exc
    return DeregisterTaskDefinitionResult(
        task_definition=resp.get("taskDefinition"),
    )


async def describe_capacity_providers(
    *,
    capacity_providers: list[str] | None = None,
    cluster: str | None = None,
    include: list[str] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeCapacityProvidersResult:
    """Describe capacity providers.

    Args:
        capacity_providers: Capacity providers.
        cluster: Cluster.
        include: Include.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if capacity_providers is not None:
        kwargs["capacityProviders"] = capacity_providers
    if cluster is not None:
        kwargs["cluster"] = cluster
    if include is not None:
        kwargs["include"] = include
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("DescribeCapacityProviders", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe capacity providers") from exc
    return DescribeCapacityProvidersResult(
        capacity_providers=resp.get("capacityProviders"),
        failures=resp.get("failures"),
        next_token=resp.get("nextToken"),
    )


async def describe_clusters(
    *,
    clusters: list[str] | None = None,
    include: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeClustersResult:
    """Describe clusters.

    Args:
        clusters: Clusters.
        include: Include.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if clusters is not None:
        kwargs["clusters"] = clusters
    if include is not None:
        kwargs["include"] = include
    try:
        resp = await client.call("DescribeClusters", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe clusters") from exc
    return DescribeClustersResult(
        clusters=resp.get("clusters"),
        failures=resp.get("failures"),
    )


async def describe_container_instances(
    container_instances: list[str],
    *,
    cluster: str | None = None,
    include: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeContainerInstancesResult:
    """Describe container instances.

    Args:
        container_instances: Container instances.
        cluster: Cluster.
        include: Include.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["containerInstances"] = container_instances
    if cluster is not None:
        kwargs["cluster"] = cluster
    if include is not None:
        kwargs["include"] = include
    try:
        resp = await client.call("DescribeContainerInstances", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe container instances") from exc
    return DescribeContainerInstancesResult(
        container_instances=resp.get("containerInstances"),
        failures=resp.get("failures"),
    )


async def describe_service_deployments(
    service_deployment_arns: list[str],
    region_name: str | None = None,
) -> DescribeServiceDeploymentsResult:
    """Describe service deployments.

    Args:
        service_deployment_arns: Service deployment arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceDeploymentArns"] = service_deployment_arns
    try:
        resp = await client.call("DescribeServiceDeployments", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe service deployments") from exc
    return DescribeServiceDeploymentsResult(
        service_deployments=resp.get("serviceDeployments"),
        failures=resp.get("failures"),
    )


async def describe_service_revisions(
    service_revision_arns: list[str],
    region_name: str | None = None,
) -> DescribeServiceRevisionsResult:
    """Describe service revisions.

    Args:
        service_revision_arns: Service revision arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceRevisionArns"] = service_revision_arns
    try:
        resp = await client.call("DescribeServiceRevisions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe service revisions") from exc
    return DescribeServiceRevisionsResult(
        service_revisions=resp.get("serviceRevisions"),
        failures=resp.get("failures"),
    )


async def describe_task_sets(
    cluster: str,
    service: str,
    *,
    task_sets: list[str] | None = None,
    include: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeTaskSetsResult:
    """Describe task sets.

    Args:
        cluster: Cluster.
        service: Service.
        task_sets: Task sets.
        include: Include.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["cluster"] = cluster
    kwargs["service"] = service
    if task_sets is not None:
        kwargs["taskSets"] = task_sets
    if include is not None:
        kwargs["include"] = include
    try:
        resp = await client.call("DescribeTaskSets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe task sets") from exc
    return DescribeTaskSetsResult(
        task_sets=resp.get("taskSets"),
        failures=resp.get("failures"),
    )


async def discover_poll_endpoint(
    *,
    container_instance: str | None = None,
    cluster: str | None = None,
    region_name: str | None = None,
) -> DiscoverPollEndpointResult:
    """Discover poll endpoint.

    Args:
        container_instance: Container instance.
        cluster: Cluster.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if container_instance is not None:
        kwargs["containerInstance"] = container_instance
    if cluster is not None:
        kwargs["cluster"] = cluster
    try:
        resp = await client.call("DiscoverPollEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to discover poll endpoint") from exc
    return DiscoverPollEndpointResult(
        endpoint=resp.get("endpoint"),
        telemetry_endpoint=resp.get("telemetryEndpoint"),
        service_connect_endpoint=resp.get("serviceConnectEndpoint"),
    )


async def execute_command(
    command: str,
    interactive: bool,
    task: str,
    *,
    cluster: str | None = None,
    container: str | None = None,
    region_name: str | None = None,
) -> ExecuteCommandResult:
    """Execute command.

    Args:
        command: Command.
        interactive: Interactive.
        task: Task.
        cluster: Cluster.
        container: Container.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["command"] = command
    kwargs["interactive"] = interactive
    kwargs["task"] = task
    if cluster is not None:
        kwargs["cluster"] = cluster
    if container is not None:
        kwargs["container"] = container
    try:
        resp = await client.call("ExecuteCommand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to execute command") from exc
    return ExecuteCommandResult(
        cluster_arn=resp.get("clusterArn"),
        container_arn=resp.get("containerArn"),
        container_name=resp.get("containerName"),
        interactive=resp.get("interactive"),
        session=resp.get("session"),
        task_arn=resp.get("taskArn"),
    )


async def get_task_protection(
    cluster: str,
    *,
    tasks: list[str] | None = None,
    region_name: str | None = None,
) -> GetTaskProtectionResult:
    """Get task protection.

    Args:
        cluster: Cluster.
        tasks: Tasks.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["cluster"] = cluster
    if tasks is not None:
        kwargs["tasks"] = tasks
    try:
        resp = await client.call("GetTaskProtection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get task protection") from exc
    return GetTaskProtectionResult(
        protected_tasks=resp.get("protectedTasks"),
        failures=resp.get("failures"),
    )


async def list_account_settings(
    *,
    name: str | None = None,
    value: str | None = None,
    principal_arn: str | None = None,
    effective_settings: bool | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAccountSettingsResult:
    """List account settings.

    Args:
        name: Name.
        value: Value.
        principal_arn: Principal arn.
        effective_settings: Effective settings.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["name"] = name
    if value is not None:
        kwargs["value"] = value
    if principal_arn is not None:
        kwargs["principalArn"] = principal_arn
    if effective_settings is not None:
        kwargs["effectiveSettings"] = effective_settings
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListAccountSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list account settings") from exc
    return ListAccountSettingsResult(
        settings=resp.get("settings"),
        next_token=resp.get("nextToken"),
    )


async def list_attributes(
    target_type: str,
    *,
    cluster: str | None = None,
    attribute_name: str | None = None,
    attribute_value: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAttributesResult:
    """List attributes.

    Args:
        target_type: Target type.
        cluster: Cluster.
        attribute_name: Attribute name.
        attribute_value: Attribute value.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["targetType"] = target_type
    if cluster is not None:
        kwargs["cluster"] = cluster
    if attribute_name is not None:
        kwargs["attributeName"] = attribute_name
    if attribute_value is not None:
        kwargs["attributeValue"] = attribute_value
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list attributes") from exc
    return ListAttributesResult(
        attributes=resp.get("attributes"),
        next_token=resp.get("nextToken"),
    )


async def list_container_instances(
    *,
    cluster: str | None = None,
    filter: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> ListContainerInstancesResult:
    """List container instances.

    Args:
        cluster: Cluster.
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if cluster is not None:
        kwargs["cluster"] = cluster
    if filter is not None:
        kwargs["filter"] = filter
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if status is not None:
        kwargs["status"] = status
    try:
        resp = await client.call("ListContainerInstances", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list container instances") from exc
    return ListContainerInstancesResult(
        container_instance_arns=resp.get("containerInstanceArns"),
        next_token=resp.get("nextToken"),
    )


async def list_service_deployments(
    service: str,
    *,
    cluster: str | None = None,
    status: list[str] | None = None,
    created_at: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListServiceDeploymentsResult:
    """List service deployments.

    Args:
        service: Service.
        cluster: Cluster.
        status: Status.
        created_at: Created at.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["service"] = service
    if cluster is not None:
        kwargs["cluster"] = cluster
    if status is not None:
        kwargs["status"] = status
    if created_at is not None:
        kwargs["createdAt"] = created_at
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListServiceDeployments", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list service deployments") from exc
    return ListServiceDeploymentsResult(
        service_deployments=resp.get("serviceDeployments"),
        next_token=resp.get("nextToken"),
    )


async def list_services(
    *,
    cluster: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    launch_type: str | None = None,
    scheduling_strategy: str | None = None,
    region_name: str | None = None,
) -> ListServicesResult:
    """List services.

    Args:
        cluster: Cluster.
        next_token: Next token.
        max_results: Max results.
        launch_type: Launch type.
        scheduling_strategy: Scheduling strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if cluster is not None:
        kwargs["cluster"] = cluster
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if launch_type is not None:
        kwargs["launchType"] = launch_type
    if scheduling_strategy is not None:
        kwargs["schedulingStrategy"] = scheduling_strategy
    try:
        resp = await client.call("ListServices", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list services") from exc
    return ListServicesResult(
        service_arns=resp.get("serviceArns"),
        next_token=resp.get("nextToken"),
    )


async def list_services_by_namespace(
    namespace: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListServicesByNamespaceResult:
    """List services by namespace.

    Args:
        namespace: Namespace.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["namespace"] = namespace
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListServicesByNamespace", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list services by namespace") from exc
    return ListServicesByNamespaceResult(
        service_arns=resp.get("serviceArns"),
        next_token=resp.get("nextToken"),
    )


async def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def list_task_definition_families(
    *,
    family_prefix: str | None = None,
    status: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTaskDefinitionFamiliesResult:
    """List task definition families.

    Args:
        family_prefix: Family prefix.
        status: Status.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if family_prefix is not None:
        kwargs["familyPrefix"] = family_prefix
    if status is not None:
        kwargs["status"] = status
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListTaskDefinitionFamilies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list task definition families") from exc
    return ListTaskDefinitionFamiliesResult(
        families=resp.get("families"),
        next_token=resp.get("nextToken"),
    )


async def list_task_definitions(
    *,
    family_prefix: str | None = None,
    status: str | None = None,
    sort: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTaskDefinitionsResult:
    """List task definitions.

    Args:
        family_prefix: Family prefix.
        status: Status.
        sort: Sort.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if family_prefix is not None:
        kwargs["familyPrefix"] = family_prefix
    if status is not None:
        kwargs["status"] = status
    if sort is not None:
        kwargs["sort"] = sort
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListTaskDefinitions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list task definitions") from exc
    return ListTaskDefinitionsResult(
        task_definition_arns=resp.get("taskDefinitionArns"),
        next_token=resp.get("nextToken"),
    )


async def put_account_setting(
    name: str,
    value: str,
    *,
    principal_arn: str | None = None,
    region_name: str | None = None,
) -> PutAccountSettingResult:
    """Put account setting.

    Args:
        name: Name.
        value: Value.
        principal_arn: Principal arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["value"] = value
    if principal_arn is not None:
        kwargs["principalArn"] = principal_arn
    try:
        resp = await client.call("PutAccountSetting", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put account setting") from exc
    return PutAccountSettingResult(
        setting=resp.get("setting"),
    )


async def put_account_setting_default(
    name: str,
    value: str,
    region_name: str | None = None,
) -> PutAccountSettingDefaultResult:
    """Put account setting default.

    Args:
        name: Name.
        value: Value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["value"] = value
    try:
        resp = await client.call("PutAccountSettingDefault", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put account setting default") from exc
    return PutAccountSettingDefaultResult(
        setting=resp.get("setting"),
    )


async def put_attributes(
    attributes: list[dict[str, Any]],
    *,
    cluster: str | None = None,
    region_name: str | None = None,
) -> PutAttributesResult:
    """Put attributes.

    Args:
        attributes: Attributes.
        cluster: Cluster.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["attributes"] = attributes
    if cluster is not None:
        kwargs["cluster"] = cluster
    try:
        resp = await client.call("PutAttributes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put attributes") from exc
    return PutAttributesResult(
        attributes=resp.get("attributes"),
    )


async def put_cluster_capacity_providers(
    cluster: str,
    capacity_providers: list[str],
    default_capacity_provider_strategy: list[dict[str, Any]],
    region_name: str | None = None,
) -> PutClusterCapacityProvidersResult:
    """Put cluster capacity providers.

    Args:
        cluster: Cluster.
        capacity_providers: Capacity providers.
        default_capacity_provider_strategy: Default capacity provider strategy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["cluster"] = cluster
    kwargs["capacityProviders"] = capacity_providers
    kwargs["defaultCapacityProviderStrategy"] = default_capacity_provider_strategy
    try:
        resp = await client.call("PutClusterCapacityProviders", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put cluster capacity providers") from exc
    return PutClusterCapacityProvidersResult(
        cluster=resp.get("cluster"),
    )


async def register_container_instance(
    *,
    cluster: str | None = None,
    instance_identity_document: str | None = None,
    instance_identity_document_signature: str | None = None,
    total_resources: list[dict[str, Any]] | None = None,
    version_info: dict[str, Any] | None = None,
    container_instance_arn: str | None = None,
    attributes: list[dict[str, Any]] | None = None,
    platform_devices: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> RegisterContainerInstanceResult:
    """Register container instance.

    Args:
        cluster: Cluster.
        instance_identity_document: Instance identity document.
        instance_identity_document_signature: Instance identity document signature.
        total_resources: Total resources.
        version_info: Version info.
        container_instance_arn: Container instance arn.
        attributes: Attributes.
        platform_devices: Platform devices.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if cluster is not None:
        kwargs["cluster"] = cluster
    if instance_identity_document is not None:
        kwargs["instanceIdentityDocument"] = instance_identity_document
    if instance_identity_document_signature is not None:
        kwargs["instanceIdentityDocumentSignature"] = instance_identity_document_signature
    if total_resources is not None:
        kwargs["totalResources"] = total_resources
    if version_info is not None:
        kwargs["versionInfo"] = version_info
    if container_instance_arn is not None:
        kwargs["containerInstanceArn"] = container_instance_arn
    if attributes is not None:
        kwargs["attributes"] = attributes
    if platform_devices is not None:
        kwargs["platformDevices"] = platform_devices
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("RegisterContainerInstance", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register container instance") from exc
    return RegisterContainerInstanceResult(
        container_instance=resp.get("containerInstance"),
    )


async def register_task_definition(
    family: str,
    container_definitions: list[dict[str, Any]],
    *,
    task_role_arn: str | None = None,
    execution_role_arn: str | None = None,
    network_mode: str | None = None,
    volumes: list[dict[str, Any]] | None = None,
    placement_constraints: list[dict[str, Any]] | None = None,
    requires_compatibilities: list[str] | None = None,
    cpu: str | None = None,
    memory: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    pid_mode: str | None = None,
    ipc_mode: str | None = None,
    proxy_configuration: dict[str, Any] | None = None,
    inference_accelerators: list[dict[str, Any]] | None = None,
    ephemeral_storage: dict[str, Any] | None = None,
    runtime_platform: dict[str, Any] | None = None,
    enable_fault_injection: bool | None = None,
    region_name: str | None = None,
) -> RegisterTaskDefinitionResult:
    """Register task definition.

    Args:
        family: Family.
        container_definitions: Container definitions.
        task_role_arn: Task role arn.
        execution_role_arn: Execution role arn.
        network_mode: Network mode.
        volumes: Volumes.
        placement_constraints: Placement constraints.
        requires_compatibilities: Requires compatibilities.
        cpu: Cpu.
        memory: Memory.
        tags: Tags.
        pid_mode: Pid mode.
        ipc_mode: Ipc mode.
        proxy_configuration: Proxy configuration.
        inference_accelerators: Inference accelerators.
        ephemeral_storage: Ephemeral storage.
        runtime_platform: Runtime platform.
        enable_fault_injection: Enable fault injection.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["family"] = family
    kwargs["containerDefinitions"] = container_definitions
    if task_role_arn is not None:
        kwargs["taskRoleArn"] = task_role_arn
    if execution_role_arn is not None:
        kwargs["executionRoleArn"] = execution_role_arn
    if network_mode is not None:
        kwargs["networkMode"] = network_mode
    if volumes is not None:
        kwargs["volumes"] = volumes
    if placement_constraints is not None:
        kwargs["placementConstraints"] = placement_constraints
    if requires_compatibilities is not None:
        kwargs["requiresCompatibilities"] = requires_compatibilities
    if cpu is not None:
        kwargs["cpu"] = cpu
    if memory is not None:
        kwargs["memory"] = memory
    if tags is not None:
        kwargs["tags"] = tags
    if pid_mode is not None:
        kwargs["pidMode"] = pid_mode
    if ipc_mode is not None:
        kwargs["ipcMode"] = ipc_mode
    if proxy_configuration is not None:
        kwargs["proxyConfiguration"] = proxy_configuration
    if inference_accelerators is not None:
        kwargs["inferenceAccelerators"] = inference_accelerators
    if ephemeral_storage is not None:
        kwargs["ephemeralStorage"] = ephemeral_storage
    if runtime_platform is not None:
        kwargs["runtimePlatform"] = runtime_platform
    if enable_fault_injection is not None:
        kwargs["enableFaultInjection"] = enable_fault_injection
    try:
        resp = await client.call("RegisterTaskDefinition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register task definition") from exc
    return RegisterTaskDefinitionResult(
        task_definition=resp.get("taskDefinition"),
        tags=resp.get("tags"),
    )


async def start_task(
    container_instances: list[str],
    task_definition: str,
    *,
    cluster: str | None = None,
    enable_ecs_managed_tags: bool | None = None,
    enable_execute_command: bool | None = None,
    group: str | None = None,
    network_configuration: dict[str, Any] | None = None,
    overrides: dict[str, Any] | None = None,
    propagate_tags: str | None = None,
    reference_id: str | None = None,
    started_by: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    volume_configurations: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> StartTaskResult:
    """Start task.

    Args:
        container_instances: Container instances.
        task_definition: Task definition.
        cluster: Cluster.
        enable_ecs_managed_tags: Enable ecs managed tags.
        enable_execute_command: Enable execute command.
        group: Group.
        network_configuration: Network configuration.
        overrides: Overrides.
        propagate_tags: Propagate tags.
        reference_id: Reference id.
        started_by: Started by.
        tags: Tags.
        volume_configurations: Volume configurations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["containerInstances"] = container_instances
    kwargs["taskDefinition"] = task_definition
    if cluster is not None:
        kwargs["cluster"] = cluster
    if enable_ecs_managed_tags is not None:
        kwargs["enableECSManagedTags"] = enable_ecs_managed_tags
    if enable_execute_command is not None:
        kwargs["enableExecuteCommand"] = enable_execute_command
    if group is not None:
        kwargs["group"] = group
    if network_configuration is not None:
        kwargs["networkConfiguration"] = network_configuration
    if overrides is not None:
        kwargs["overrides"] = overrides
    if propagate_tags is not None:
        kwargs["propagateTags"] = propagate_tags
    if reference_id is not None:
        kwargs["referenceId"] = reference_id
    if started_by is not None:
        kwargs["startedBy"] = started_by
    if tags is not None:
        kwargs["tags"] = tags
    if volume_configurations is not None:
        kwargs["volumeConfigurations"] = volume_configurations
    try:
        resp = await client.call("StartTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start task") from exc
    return StartTaskResult(
        tasks=resp.get("tasks"),
        failures=resp.get("failures"),
    )


async def stop_service_deployment(
    service_deployment_arn: str,
    *,
    stop_type: str | None = None,
    region_name: str | None = None,
) -> StopServiceDeploymentResult:
    """Stop service deployment.

    Args:
        service_deployment_arn: Service deployment arn.
        stop_type: Stop type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["serviceDeploymentArn"] = service_deployment_arn
    if stop_type is not None:
        kwargs["stopType"] = stop_type
    try:
        resp = await client.call("StopServiceDeployment", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop service deployment") from exc
    return StopServiceDeploymentResult(
        service_deployment_arn=resp.get("serviceDeploymentArn"),
    )


async def submit_attachment_state_changes(
    attachments: list[dict[str, Any]],
    *,
    cluster: str | None = None,
    region_name: str | None = None,
) -> SubmitAttachmentStateChangesResult:
    """Submit attachment state changes.

    Args:
        attachments: Attachments.
        cluster: Cluster.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["attachments"] = attachments
    if cluster is not None:
        kwargs["cluster"] = cluster
    try:
        resp = await client.call("SubmitAttachmentStateChanges", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to submit attachment state changes") from exc
    return SubmitAttachmentStateChangesResult(
        acknowledgment=resp.get("acknowledgment"),
    )


async def submit_container_state_change(
    *,
    cluster: str | None = None,
    task: str | None = None,
    container_name: str | None = None,
    runtime_id: str | None = None,
    status: str | None = None,
    exit_code: int | None = None,
    reason: str | None = None,
    network_bindings: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> SubmitContainerStateChangeResult:
    """Submit container state change.

    Args:
        cluster: Cluster.
        task: Task.
        container_name: Container name.
        runtime_id: Runtime id.
        status: Status.
        exit_code: Exit code.
        reason: Reason.
        network_bindings: Network bindings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if cluster is not None:
        kwargs["cluster"] = cluster
    if task is not None:
        kwargs["task"] = task
    if container_name is not None:
        kwargs["containerName"] = container_name
    if runtime_id is not None:
        kwargs["runtimeId"] = runtime_id
    if status is not None:
        kwargs["status"] = status
    if exit_code is not None:
        kwargs["exitCode"] = exit_code
    if reason is not None:
        kwargs["reason"] = reason
    if network_bindings is not None:
        kwargs["networkBindings"] = network_bindings
    try:
        resp = await client.call("SubmitContainerStateChange", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to submit container state change") from exc
    return SubmitContainerStateChangeResult(
        acknowledgment=resp.get("acknowledgment"),
    )


async def submit_task_state_change(
    *,
    cluster: str | None = None,
    task: str | None = None,
    status: str | None = None,
    reason: str | None = None,
    containers: list[dict[str, Any]] | None = None,
    attachments: list[dict[str, Any]] | None = None,
    managed_agents: list[dict[str, Any]] | None = None,
    pull_started_at: str | None = None,
    pull_stopped_at: str | None = None,
    execution_stopped_at: str | None = None,
    region_name: str | None = None,
) -> SubmitTaskStateChangeResult:
    """Submit task state change.

    Args:
        cluster: Cluster.
        task: Task.
        status: Status.
        reason: Reason.
        containers: Containers.
        attachments: Attachments.
        managed_agents: Managed agents.
        pull_started_at: Pull started at.
        pull_stopped_at: Pull stopped at.
        execution_stopped_at: Execution stopped at.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    if cluster is not None:
        kwargs["cluster"] = cluster
    if task is not None:
        kwargs["task"] = task
    if status is not None:
        kwargs["status"] = status
    if reason is not None:
        kwargs["reason"] = reason
    if containers is not None:
        kwargs["containers"] = containers
    if attachments is not None:
        kwargs["attachments"] = attachments
    if managed_agents is not None:
        kwargs["managedAgents"] = managed_agents
    if pull_started_at is not None:
        kwargs["pullStartedAt"] = pull_started_at
    if pull_stopped_at is not None:
        kwargs["pullStoppedAt"] = pull_stopped_at
    if execution_stopped_at is not None:
        kwargs["executionStoppedAt"] = execution_stopped_at
    try:
        resp = await client.call("SubmitTaskStateChange", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to submit task state change") from exc
    return SubmitTaskStateChangeResult(
        acknowledgment=resp.get("acknowledgment"),
    )


async def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_capacity_provider(
    name: str,
    *,
    cluster: str | None = None,
    auto_scaling_group_provider: dict[str, Any] | None = None,
    managed_instances_provider: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateCapacityProviderResult:
    """Update capacity provider.

    Args:
        name: Name.
        cluster: Cluster.
        auto_scaling_group_provider: Auto scaling group provider.
        managed_instances_provider: Managed instances provider.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if cluster is not None:
        kwargs["cluster"] = cluster
    if auto_scaling_group_provider is not None:
        kwargs["autoScalingGroupProvider"] = auto_scaling_group_provider
    if managed_instances_provider is not None:
        kwargs["managedInstancesProvider"] = managed_instances_provider
    try:
        resp = await client.call("UpdateCapacityProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update capacity provider") from exc
    return UpdateCapacityProviderResult(
        capacity_provider=resp.get("capacityProvider"),
    )


async def update_cluster(
    cluster: str,
    *,
    settings: list[dict[str, Any]] | None = None,
    configuration: dict[str, Any] | None = None,
    service_connect_defaults: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateClusterResult:
    """Update cluster.

    Args:
        cluster: Cluster.
        settings: Settings.
        configuration: Configuration.
        service_connect_defaults: Service connect defaults.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["cluster"] = cluster
    if settings is not None:
        kwargs["settings"] = settings
    if configuration is not None:
        kwargs["configuration"] = configuration
    if service_connect_defaults is not None:
        kwargs["serviceConnectDefaults"] = service_connect_defaults
    try:
        resp = await client.call("UpdateCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update cluster") from exc
    return UpdateClusterResult(
        cluster=resp.get("cluster"),
    )


async def update_cluster_settings(
    cluster: str,
    settings: list[dict[str, Any]],
    region_name: str | None = None,
) -> UpdateClusterSettingsResult:
    """Update cluster settings.

    Args:
        cluster: Cluster.
        settings: Settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["cluster"] = cluster
    kwargs["settings"] = settings
    try:
        resp = await client.call("UpdateClusterSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update cluster settings") from exc
    return UpdateClusterSettingsResult(
        cluster=resp.get("cluster"),
    )


async def update_container_agent(
    container_instance: str,
    *,
    cluster: str | None = None,
    region_name: str | None = None,
) -> UpdateContainerAgentResult:
    """Update container agent.

    Args:
        container_instance: Container instance.
        cluster: Cluster.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["containerInstance"] = container_instance
    if cluster is not None:
        kwargs["cluster"] = cluster
    try:
        resp = await client.call("UpdateContainerAgent", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update container agent") from exc
    return UpdateContainerAgentResult(
        container_instance=resp.get("containerInstance"),
    )


async def update_container_instances_state(
    container_instances: list[str],
    status: str,
    *,
    cluster: str | None = None,
    region_name: str | None = None,
) -> UpdateContainerInstancesStateResult:
    """Update container instances state.

    Args:
        container_instances: Container instances.
        status: Status.
        cluster: Cluster.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["containerInstances"] = container_instances
    kwargs["status"] = status
    if cluster is not None:
        kwargs["cluster"] = cluster
    try:
        resp = await client.call("UpdateContainerInstancesState", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update container instances state") from exc
    return UpdateContainerInstancesStateResult(
        container_instances=resp.get("containerInstances"),
        failures=resp.get("failures"),
    )


async def update_service_primary_task_set(
    cluster: str,
    service: str,
    primary_task_set: str,
    region_name: str | None = None,
) -> UpdateServicePrimaryTaskSetResult:
    """Update service primary task set.

    Args:
        cluster: Cluster.
        service: Service.
        primary_task_set: Primary task set.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["cluster"] = cluster
    kwargs["service"] = service
    kwargs["primaryTaskSet"] = primary_task_set
    try:
        resp = await client.call("UpdateServicePrimaryTaskSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update service primary task set") from exc
    return UpdateServicePrimaryTaskSetResult(
        task_set=resp.get("taskSet"),
    )


async def update_task_protection(
    cluster: str,
    tasks: list[str],
    protection_enabled: bool,
    *,
    expires_in_minutes: int | None = None,
    region_name: str | None = None,
) -> UpdateTaskProtectionResult:
    """Update task protection.

    Args:
        cluster: Cluster.
        tasks: Tasks.
        protection_enabled: Protection enabled.
        expires_in_minutes: Expires in minutes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["cluster"] = cluster
    kwargs["tasks"] = tasks
    kwargs["protectionEnabled"] = protection_enabled
    if expires_in_minutes is not None:
        kwargs["expiresInMinutes"] = expires_in_minutes
    try:
        resp = await client.call("UpdateTaskProtection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update task protection") from exc
    return UpdateTaskProtectionResult(
        protected_tasks=resp.get("protectedTasks"),
        failures=resp.get("failures"),
    )


async def update_task_set(
    cluster: str,
    service: str,
    task_set: str,
    scale: dict[str, Any],
    region_name: str | None = None,
) -> UpdateTaskSetResult:
    """Update task set.

    Args:
        cluster: Cluster.
        service: Service.
        task_set: Task set.
        scale: Scale.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("ecs", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["cluster"] = cluster
    kwargs["service"] = service
    kwargs["taskSet"] = task_set
    kwargs["scale"] = scale
    try:
        resp = await client.call("UpdateTaskSet", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update task set") from exc
    return UpdateTaskSetResult(
        task_set=resp.get("taskSet"),
    )
