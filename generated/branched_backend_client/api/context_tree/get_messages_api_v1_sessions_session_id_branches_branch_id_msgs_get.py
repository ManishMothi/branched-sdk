from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.tree_node_read import TreeNodeRead
from ...types import Response


def _get_kwargs(
    session_id: UUID,
    branch_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/sessions/{session_id}/branches/{branch_id}/msgs",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, HTTPValidationError, list["TreeNodeRead"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TreeNodeRead.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[ErrorResponse, HTTPValidationError, list["TreeNodeRead"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: UUID,
    branch_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ErrorResponse, HTTPValidationError, list["TreeNodeRead"]]]:
    """Get Messages

     Retrieve all direct child nodes (messages) for a given branch, in chronological order

    Args:
        session_id: The ID of the session
        branch_id: The ID of the branch to get messages from

    Returns:
        List[TreeNodeRead]: List of message nodes in chronological order

    Raises:
        HTTPException: If the branch is not found or an error occurs

    Args:
        session_id (UUID):
        branch_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, HTTPValidationError, list['TreeNodeRead']]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        branch_id=branch_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: UUID,
    branch_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ErrorResponse, HTTPValidationError, list["TreeNodeRead"]]]:
    """Get Messages

     Retrieve all direct child nodes (messages) for a given branch, in chronological order

    Args:
        session_id: The ID of the session
        branch_id: The ID of the branch to get messages from

    Returns:
        List[TreeNodeRead]: List of message nodes in chronological order

    Raises:
        HTTPException: If the branch is not found or an error occurs

    Args:
        session_id (UUID):
        branch_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, HTTPValidationError, list['TreeNodeRead']]
    """

    return sync_detailed(
        session_id=session_id,
        branch_id=branch_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    session_id: UUID,
    branch_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ErrorResponse, HTTPValidationError, list["TreeNodeRead"]]]:
    """Get Messages

     Retrieve all direct child nodes (messages) for a given branch, in chronological order

    Args:
        session_id: The ID of the session
        branch_id: The ID of the branch to get messages from

    Returns:
        List[TreeNodeRead]: List of message nodes in chronological order

    Raises:
        HTTPException: If the branch is not found or an error occurs

    Args:
        session_id (UUID):
        branch_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, HTTPValidationError, list['TreeNodeRead']]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        branch_id=branch_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: UUID,
    branch_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ErrorResponse, HTTPValidationError, list["TreeNodeRead"]]]:
    """Get Messages

     Retrieve all direct child nodes (messages) for a given branch, in chronological order

    Args:
        session_id: The ID of the session
        branch_id: The ID of the branch to get messages from

    Returns:
        List[TreeNodeRead]: List of message nodes in chronological order

    Raises:
        HTTPException: If the branch is not found or an error occurs

    Args:
        session_id (UUID):
        branch_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, HTTPValidationError, list['TreeNodeRead']]
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            branch_id=branch_id,
            client=client,
        )
    ).parsed
