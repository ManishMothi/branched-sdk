from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.chat_session_create import ChatSessionCreate
from ...models.chat_session_read import ChatSessionRead
from ...models.error_response import ErrorResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: ChatSessionCreate,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/sessions",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = ChatSessionRead.from_dict(response.json())

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
) -> Response[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ChatSessionCreate,
) -> Response[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    r"""Post Session

     Starts a new conversation \"session\" with an initial message and gets an LLM response.

    Args:
        payload: Contains the initial message for the conversation
        user_id: The ID of the user creating the session

    Returns:
        ChatSessionRead: The newly created chat session with the first message and response

    Raises:
        HTTPException: If there's an error creating the session or generating the response

    Args:
        body (ChatSessionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: ChatSessionCreate,
) -> Optional[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    r"""Post Session

     Starts a new conversation \"session\" with an initial message and gets an LLM response.

    Args:
        payload: Contains the initial message for the conversation
        user_id: The ID of the user creating the session

    Returns:
        ChatSessionRead: The newly created chat session with the first message and response

    Raises:
        HTTPException: If there's an error creating the session or generating the response

    Args:
        body (ChatSessionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChatSessionRead, ErrorResponse, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ChatSessionCreate,
) -> Response[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    r"""Post Session

     Starts a new conversation \"session\" with an initial message and gets an LLM response.

    Args:
        payload: Contains the initial message for the conversation
        user_id: The ID of the user creating the session

    Returns:
        ChatSessionRead: The newly created chat session with the first message and response

    Raises:
        HTTPException: If there's an error creating the session or generating the response

    Args:
        body (ChatSessionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ChatSessionCreate,
) -> Optional[Union[ChatSessionRead, ErrorResponse, HTTPValidationError]]:
    r"""Post Session

     Starts a new conversation \"session\" with an initial message and gets an LLM response.

    Args:
        payload: Contains the initial message for the conversation
        user_id: The ID of the user creating the session

    Returns:
        ChatSessionRead: The newly created chat session with the first message and response

    Raises:
        HTTPException: If there's an error creating the session or generating the response

    Args:
        body (ChatSessionCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChatSessionRead, ErrorResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
