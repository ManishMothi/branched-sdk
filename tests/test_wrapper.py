from re import M
import pytest
from uuid import UUID
from unittest.mock import MagicMock

from branched_sdk.wrapper import BranchedClient, BranchedError
from generated.branched_backend_client.models import ChatSessionRead, ErrorResponse
from generated.branched_backend_client.models.tree_node_read import TreeNodeRead

# Test data constants
TEST_SESSION_ID = UUID("12345678-1234-5678-1234-567812345678")
TEST_BRANCH_ID = UUID("87654321-4321-5678-1234-567812345678")
TEST_USER_ID = "user_12345"
TEST_MESSAGE = "Test message"


class MockResponse:
    def __init__(self, status_code, parsed=None):
        self.status_code = status_code
        self.parsed = parsed
        self.headers = {}
        
    def json(self):
        if self.parsed:
            return self.parsed.to_dict()
        return {}


@pytest.fixture
def mock_client() -> BranchedClient:
    return BranchedClient(api_key="testkey")


def test_create_session_success(monkeypatch, mock_client: BranchedClient):
    # Mock the response from the API

    mock_tree_node_read = TreeNodeRead(
        id=TEST_BRANCH_ID,
        chat_session_id=TEST_SESSION_ID,
        parent_id=None,
        user_message=TEST_MESSAGE,
        llm_response="LLM response",
        created_at="2023-01-01T00:00:00Z",
        children=[]
    )

    mock_chat_session_read = ChatSessionRead(
        id=TEST_SESSION_ID,
        user_id=TEST_USER_ID,
        created_at="2023-01-01T00:00:00Z",
        nodes=[mock_tree_node_read]
    )
    
    def mock_post_session(*args, **kwargs):
        return MockResponse(status_code=201, parsed=mock_chat_session_read)
    
    # mock _post_session
    mock = MagicMock(side_effect=mock_post_session)
    monkeypatch.setattr(
        "branched_sdk.wrapper._post_session", 
        mock
    )
    
    response = mock_client.create_session(TEST_MESSAGE)
        
    assert isinstance(response, ChatSessionRead)
    assert response.id == TEST_SESSION_ID
    assert len(response.nodes) == 1
    assert response.nodes[0].user_message == "Test message"
    assert response.nodes[0].parent_id == None

    # Verify the mock was called correctly
    mock.assert_called_once()


def test_create_session_error(monkeypatch, mock_client: BranchedClient):
    # Test case for 400 error
    error_response = ErrorResponse(
        detail="Invalid request: initial message cannot be empty",
        error_code=400,
        error_type="validation_error"
    )
    
    def mock_post_session_error(client, body):
        return MockResponse(status_code=400, parsed=error_response)
    
    # Patch the _post_session function
    monkeypatch.setattr("branched_sdk.wrapper._post_session", mock_post_session_error)
    
    # Test that the correct error is raised
    with pytest.raises(BranchedError) as exc_info:
        mock_client.create_session("")  # Empty string to trigger error
    
    # Verify the error details
    assert exc_info.value.code == 400
    assert "Invalid request" in str(exc_info.value.detail)
    
    # Test exception handling
    def mock_raise_exception(*args, **kwargs):
        raise Exception("Connection error")
    
    monkeypatch.setattr("branched_sdk.wrapper._post_session", mock_raise_exception)
    
    with pytest.raises(BranchedError) as exc_info:
        mock_client.create_session("test")
    assert "Connection error" in str(exc_info.value)


def test_create_branch_success(monkeypatch, mock_client: BranchedClient):
    # Mock response
    mock_branch = TreeNodeRead(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        chat_session_id=TEST_SESSION_ID,
        parent_id=UUID("22222222-2222-2222-2222-222222222222"),
        user_message="User message",
        llm_response="LLM response",
        created_at="2023-01-01T00:00:00Z",
        children=[]
    )
    
    def mock_post_branch(*args, **kwargs):
        return MockResponse(status_code=201, parsed=mock_branch)
    
    monkeypatch.setattr("branched_sdk.wrapper._post_branch", MagicMock(side_effect=mock_post_branch))
    
    response = mock_client.create_branch(
        session_id=TEST_SESSION_ID,
        parent_id=UUID("22222222-2222-2222-2222-222222222222"),
        user_message="User message"
    )
    
    assert isinstance(response, TreeNodeRead)
    assert response.id == UUID("11111111-1111-1111-1111-111111111111")
    assert response.chat_session_id == TEST_SESSION_ID

def test_create_branch_error(monkeypatch, mock_client: BranchedClient):
    error_response = ErrorResponse(
        detail="Invalid parent ID",
        error_code=400,
        error_type="validation_error"
    )
    
    def mock_post_branch_error(*args, **kwargs):
        return MockResponse(status_code=400, parsed=error_response)
    
    monkeypatch.setattr("branched_sdk.wrapper._post_branch", MagicMock(side_effect=mock_post_branch_error))
    
    with pytest.raises(BranchedError) as exc_info:
        mock_client.create_branch(
            session_id=TEST_SESSION_ID,
            parent_id=UUID("11111111-1111-1111-1111-111111111112"),
            user_message="Test"
        )
    
    assert exc_info.value.code == 400
    assert "Invalid parent ID" in str(exc_info.value.detail)


def test_delete_session_success(monkeypatch, mock_client: BranchedClient):
    def mock_delete_session(*args, **kwargs):
        return MockResponse(status_code=204, parsed=None)
    
    monkeypatch.setattr("branched_sdk.wrapper._delete_session", MagicMock(side_effect=mock_delete_session))
    
    # Should not raise
    mock_client.delete_session(TEST_SESSION_ID)

def test_delete_session_error(monkeypatch, mock_client: BranchedClient):
    error_response = ErrorResponse(
        detail="Session not found",
        error_code=404,
        error_type="not_found"
    )
    
    def mock_delete_session_error(*args, **kwargs):
        return MockResponse(status_code=404, parsed=error_response)
    
    monkeypatch.setattr("branched_sdk.wrapper._delete_session", MagicMock(side_effect=mock_delete_session_error))
    
    with pytest.raises(BranchedError) as exc_info:
        mock_client.delete_session(TEST_SESSION_ID)
    
    assert exc_info.value.code == 404
    assert "Session not found" in str(exc_info.value.detail)


def test_delete_branch_success(monkeypatch, mock_client: BranchedClient):
    def mock_delete_branch(*args, **kwargs):
        return MockResponse(status_code=204, parsed=None)
    
    monkeypatch.setattr("branched_sdk.wrapper._delete_branch", MagicMock(side_effect=mock_delete_branch))
    
    # Should not raise
    mock_client.delete_branch(TEST_SESSION_ID, TEST_BRANCH_ID)


def test_get_session_messages_success(monkeypatch, mock_client: BranchedClient):
    mock_messages = [
        TreeNodeRead(
            id=UUID("33333333-3333-3333-3333-333333333333"),
            chat_session_id=TEST_SESSION_ID,
            parent_id=None,
            user_message="Message 1",
            llm_response="Response 1",
            created_at="2023-01-01T00:00:00Z",
            children=[]
        )
    ]
    
    def mock_get_messages(*args, **kwargs):
        return MockResponse(status_code=200, parsed=mock_messages)
    
    monkeypatch.setattr("branched_sdk.wrapper._get_messages", MagicMock(side_effect=mock_get_messages))
    
    response = mock_client.get_session_messages(TEST_SESSION_ID, TEST_BRANCH_ID)
    
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0].user_message == "Message 1"


def test_get_sessions_success(monkeypatch, mock_client: BranchedClient):
    mock_sessions = [
        ChatSessionRead(
            id=TEST_SESSION_ID,
            user_id=TEST_USER_ID,
            created_at="2023-01-01T00:00:00Z",
            nodes=[]
        )
    ]
    
    def mock_get_my_sessions(*args, **kwargs):
        return MockResponse(status_code=200, parsed=mock_sessions)
    
    monkeypatch.setattr("branched_sdk.wrapper._get_my_sessions", MagicMock(side_effect=mock_get_my_sessions))
    
    response = mock_client.get_sessions()
    
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0].id == TEST_SESSION_ID


def test_get_session_info_success(monkeypatch, mock_client: BranchedClient):
    mock_session = ChatSessionRead(
        id=TEST_SESSION_ID,
        user_id=TEST_USER_ID,
        created_at="2023-01-01T00:00:00Z",
        nodes=[]
    )
    
    def mock_get_session(*args, **kwargs):
        return MockResponse(status_code=200, parsed=mock_session)
    
    monkeypatch.setattr("branched_sdk.wrapper._get_session_info", MagicMock(side_effect=mock_get_session))
    
    response = mock_client.get_session_info(TEST_SESSION_ID)
    
    assert isinstance(response, ChatSessionRead)
    assert response.id == TEST_SESSION_ID
    assert response.user_id == TEST_USER_ID

