from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.tree_node_create import TreeNodeCreate
from ...models.tree_node_read import TreeNodeRead
from ...types import Response


def _get_kwargs(
    session_id: UUID,
    *,
    body: TreeNodeCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/v1/sessions/{session_id}/branches",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, HTTPValidationError, TreeNodeRead]]:
    if response.status_code == 201:
        response_201 = TreeNodeRead.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, HTTPValidationError, TreeNodeRead]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
    body: TreeNodeCreate,
) -> Response[Union[ErrorResponse, HTTPValidationError, TreeNodeRead]]:
    """Post Branch

     Create a new branch with an initial message and get an LLM response

    Args:
        session_id: The ID of the session
        payload: Contains the parent node ID and the message for the new branch

    Returns:
        TreeNodeRead: The newly created branch node with message and LLM response

    Raises:
        HTTPException: If the parent node is not found, LLM service is unavailable, or an error occurs

    Args:
        session_id (UUID):
        body (TreeNodeCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, HTTPValidationError, TreeNodeRead]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
    body: TreeNodeCreate,
) -> Optional[Union[ErrorResponse, HTTPValidationError, TreeNodeRead]]:
    """Post Branch

     Create a new branch with an initial message and get an LLM response

    Args:
        session_id: The ID of the session
        payload: Contains the parent node ID and the message for the new branch

    Returns:
        TreeNodeRead: The newly created branch node with message and LLM response

    Raises:
        HTTPException: If the parent node is not found, LLM service is unavailable, or an error occurs

    Args:
        session_id (UUID):
        body (TreeNodeCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, HTTPValidationError, TreeNodeRead]
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
    body: TreeNodeCreate,
) -> Response[Union[ErrorResponse, HTTPValidationError, TreeNodeRead]]:
    """Post Branch

     Create a new branch with an initial message and get an LLM response

    Args:
        session_id: The ID of the session
        payload: Contains the parent node ID and the message for the new branch

    Returns:
        TreeNodeRead: The newly created branch node with message and LLM response

    Raises:
        HTTPException: If the parent node is not found, LLM service is unavailable, or an error occurs

    Args:
        session_id (UUID):
        body (TreeNodeCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, HTTPValidationError, TreeNodeRead]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
    body: TreeNodeCreate,
) -> Optional[Union[ErrorResponse, HTTPValidationError, TreeNodeRead]]:
    """Post Branch

     Create a new branch with an initial message and get an LLM response

    Args:
        session_id: The ID of the session
        payload: Contains the parent node ID and the message for the new branch

    Returns:
        TreeNodeRead: The newly created branch node with message and LLM response

    Raises:
        HTTPException: If the parent node is not found, LLM service is unavailable, or an error occurs

    Args:
        session_id (UUID):
        body (TreeNodeCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, HTTPValidationError, TreeNodeRead]
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
            body=body,
        )
    ).parsed
