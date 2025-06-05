import os
from typing import Optional, List
from uuid import UUID

from generated.branched_backend_client.client import AuthenticatedClient as _GeneratedClient

# # key endpoint 
# from generated.branched_backend_client.api.key.generate_api_key_api_v1_keys_generate_post import sync_detailed as _gen_key
# from generated.branched_backend_client.api.key.deactivate_api_key_api_v1_keys_key_id_delete import sync_detailed as _list_keys
# from generated.branched_backend_client.api.key.list_api_keys_api_v1_keys_get import sync_detailed as _deact_key

# session endpoint
from generated.branched_backend_client.api.context_tree.delete_branch_node_route_api_v1_sessions_session_id_branches_branch_id_delete import sync_detailed as _delete_branch
from generated.branched_backend_client.api.context_tree.delete_session_route_api_v1_sessions_session_id_delete import sync_detailed as _delete_session
from generated.branched_backend_client.api.context_tree.get_messages_api_v1_sessions_session_id_branches_branch_id_msgs_get import sync_detailed as _get_messages
from generated.branched_backend_client.api.context_tree.get_my_sessions_api_v1_sessions_user_get import sync_detailed as _get_my_sessions
from generated.branched_backend_client.api.context_tree.get_session_info_api_v1_sessions_session_id_get import sync_detailed as _get_session_info
from generated.branched_backend_client.api.context_tree.health_check_api_v1_sessions_health_get import sync_detailed as _health_check
from generated.branched_backend_client.api.context_tree.post_branch_api_v1_sessions_session_id_branches_post import sync_detailed as _post_branch
from generated.branched_backend_client.api.context_tree.post_session_api_v1_sessions_post import sync_detailed as _post_session

# # api usage endpoint 
# from generated.branched_backend_client.api.api_usage.get_api_usage_route_api_v1_usage_get import sync_detailed as _get_api_usage


from generated.branched_backend_client.models.chat_session_create import ChatSessionCreate
from generated.branched_backend_client.models.chat_session_read import ChatSessionRead
from generated.branched_backend_client.models.error_response import ErrorResponse
from generated.branched_backend_client.models.http_validation_error import HTTPValidationError
from generated.branched_backend_client.models.tree_node_create import TreeNodeCreate
from generated.branched_backend_client.models.tree_node_read import TreeNodeRead
from generated.branched_backend_client.models.error_response import ErrorResponse
from generated.branched_backend_client.models.health_check_api_v1_sessions_health_get_response_health_check_api_v1_sessions_health_get import HealthCheckApiV1SessionsHealthGetResponseHealthCheckApiV1SessionsHealthGet as HealthCheckResponse

from .errors import BranchedError
from .utils import retry_on_5xx



class BranchedClient:
    """
    A thin, ergonomic wrapper around the generated client code.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 10.0,
    ):
        # Auto‐detect from env vars if not passed explicitly
        self.api_key = api_key or os.getenv("BRANCHED_API_KEY")
        if self.api_key is None:
            raise ValueError("BRANCHED_API_KEY must be provided or set as env var.")

        self.base_url = base_url or os.getenv(
            "BRANCHED_BASE_URL", "https://api.branched.com"
        )

        # Initialize the generated Client with default headers, timeouts, etc.
        self._client = _GeneratedClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}", "User-Agent": "branched-sdk/0.1.0"},
            timeout=timeout,
            token=api_key
        )

    @retry_on_5xx
    def create_session(self, initial_message: str) -> ChatSessionRead:
        """
        Create a new chat session. Returns a ChatSessionRead object.
        """
        body = ChatSessionCreate(initial_message=initial_message)
        try:
            response = _post_session(
                client=self._client,
                body=body,
            )
        except Exception as e:
            raise BranchedError.from_exception(e)

        if response.status_code >= 400:
            detail = response.parsed.detail if response.parsed else ""
            raise BranchedError.from_response(response.status_code, detail)

        return response.parsed

    @retry_on_5xx
    def create_branch(self, session_id: UUID, parent_id: UUID, user_message: str) -> TreeNodeRead:
        """
        Create a new branch off current node. Returns a TreeNodeRead object. 
        """
        body = TreeNodeCreate(parent_id=parent_id, user_message=user_message)

        try:
            response = _post_branch(
                session_id=session_id,
                client=self._client,
                body=body
            )
        except Exception as e:
            raise BranchedError.from_exception(e)

        if response.status_code >= 400:
            detail = response.parsed.detail if response.parsed else ""
            raise BranchedError.from_response(response.status_code, detail)

        return response.parsed



    @retry_on_5xx
    def delete_session(self, session_id: UUID) -> None:
        """
        Delete a chat session. Returns None if successful. 
        """
    
        try:
            response = _delete_session(
                session_id=session_id,
                client=self._client
            )
        except Exception as e:
            raise BranchedError.from_exception(e)

        if response.status_code >= 400:
            detail = response.parsed.detail if response.parsed else ""
            raise BranchedError.from_response(response.status_code, detail)

        return response.parsed


    @retry_on_5xx
    def delete_branch(self, session_id: UUID, branch_id: UUID) -> None:
        """
        Delete a specific branch and all its children. Returns None if successful. 
        """
            
        try:
            response = _delete_branch(
                session_id=session_id,
                branch_id=branch_id,
                client=self._client
            )
        except Exception as e:
            raise BranchedError.from_exception(e)

        if response.status_code >= 400:
            detail = response.parsed.detail if response.parsed else ""
            raise BranchedError.from_response(response.status_code, detail)

        return response.parsed


    @retry_on_5xx
    def get_session_messages(self, session_id: UUID, branch_id: UUID) -> List[TreeNodeRead]:
        """
        Get all direct child nodes (messages) for a given branch, in chronological order
        """
        try:
            response = _get_messages(
                session_id=session_id,
                branch_id=branch_id,
                client=self._client
            )
        except Exception as e:
            raise BranchedError.from_exception(e)

        if response.status_code >= 400:
            detail = response.parsed.detail if response.parsed else ""
            raise BranchedError.from_response(response.status_code, detail)

        return response.parsed

    @retry_on_5xx
    def get_sessions(self) -> List[ChatSessionRead]:
        """
        List all chat sessions for the current user. Returns a list of ChatSessionRead objects. 
        """ 
        try:
            response = _get_my_sessions(
                client=self._client
            )
        except Exception as e:
            raise BranchedError.from_exception(e)

        if response.status_code >= 400:
            detail = response.parsed.detail if response.parsed else ""
            raise BranchedError.from_response(response.status_code, detail)

        return response.parsed


    @retry_on_5xx
    def get_session_info(self, session_id: UUID) -> ChatSessionRead:
        """
        Retrieve session info and the list of all nodes (branches) in that session returned as ChatSessionRead object.
        """
        try:
            response = _get_session_info(
                session_id=session_id,
                client=self._client
            )
        except Exception as e:
            raise BranchedError.from_exception(e)
        

        if response.status_code >= 400:
            detail = response.parsed.detail if response.parsed else ""
            raise BranchedError.from_response(response.status_code, detail)
        
        return response.parsed 


    @retry_on_5xx
    def health_check(self) -> HealthCheckResponse:
        """
        Check if the server is healthy. Returns a HealthCheckResponse object.
        """
        try:
            response = _health_check(
                client=self._client
            )
        except Exception as e:
            raise BranchedError.from_exception(e)

        if response.status_code >= 400:
            detail = response.parsed.detail if response.parsed else ""
            raise BranchedError.from_response(response.status_code, detail)

        return response.parsed
