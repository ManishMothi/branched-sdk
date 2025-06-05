from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chat_session_read import ChatSessionRead
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    session_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/v1/sessions/{session_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ChatSessionRead.from_dict(response.json())

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
) -> Response[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
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
) -> Response[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    """Get Session Info

     Retrieve session info and the list of all nodes (branches) in that session

    Args:
        session_id: The ID of the session to retrieve

    Returns:
        ChatSessionRead: The requested chat session with its nodes

    Raises:
        HTTPException: If the session is not found or an error occurs

    Args:
        session_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    """Get Session Info

     Retrieve session info and the list of all nodes (branches) in that session

    Args:
        session_id: The ID of the session to retrieve

    Returns:
        ChatSessionRead: The requested chat session with its nodes

    Raises:
        HTTPException: If the session is not found or an error occurs

    Args:
        session_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChatSessionRead, ErrorResponse, HTTPValidationError]
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    """Get Session Info

     Retrieve session info and the list of all nodes (branches) in that session

    Args:
        session_id: The ID of the session to retrieve

    Returns:
        ChatSessionRead: The requested chat session with its nodes

    Raises:
        HTTPException: If the session is not found or an error occurs

    Args:
        session_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    """Get Session Info

     Retrieve session info and the list of all nodes (branches) in that session

    Args:
        session_id: The ID of the session to retrieve

    Returns:
        ChatSessionRead: The requested chat session with its nodes

    Raises:
        HTTPException: If the session is not found or an error occurs

    Args:
        session_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChatSessionRead, ErrorResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
        )
    ).parsed
