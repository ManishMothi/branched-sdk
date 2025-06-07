from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.health_check_api_v1_sessions_health_get_response_health_check_api_v1_sessions_health_get import (
    HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet,
)
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/v1/sessions/health",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet]]:
    if response.status_code == 200:
        response_200 = HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet.from_dict(
            response.json()
        )

        return response_200
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[ErrorResponse, HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet]]:
    """Health Check

     Basic health check returning user_id from api_key

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet]]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ErrorResponse, HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet]]:
    """Health Check

     Basic health check returning user_id from api_key

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[ErrorResponse, HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet]]:
    """Health Check

     Basic health check returning user_id from api_key

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet]]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ErrorResponse, HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet]]:
    """Health Check

     Basic health check returning user_id from api_key

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
