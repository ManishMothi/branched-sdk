# Branched Python SDK

Python client for the Branched API, providing an easy way to interact with Branched's conversation tree service.

## Installation

```bash
pip install branched-sdk
```

## Quick Start

```python
from uuid import UUID
from branched_sdk import BranchedClient, BranchedError

# Initialize the client
# Option 1: Explicit configuration
client = BranchedClient(
    api_key="your-api-key-here",
    base_url="https://branched-backend.onrender.com"
)

# Option 2: Using environment variables
# export BRANCHED_API_KEY="your-api-key-here"
# export BRANCHED_BASE_URL="https://branched-backend.onrender.com"  # optional
# client = BranchedClient()

try:
    # Create a new session
    chat_session= client.create_session("Initial message for the session")
    root_node = chat_session.nodes[0]
    print(f"Created session: {chat_session.id}")
    print(f"Root Node: {root_node.id}")

    # Create a branch in the session
    branch = client.create_branch(
        session_id=chat_session.id,
        parent_id=root_node.id,
        user_message="Let's explore this branch"
    )
    print(f"Created branch: {branch.id}")
    print(f"LLM Response: {branch.llm_response}")

    # Get session info
    session_info = client.get_session_info(session.id)
    print(f"Session info: {session_info}")

    # Get messages in a branch
    messages = client.get_session_messages(session.id, branch.id)
    print(f"Messages: {messages}")

    # List all sessions
    sessions = client.get_sessions()
    print(f"Your sessions: {sessions}")

    # Delete a session
    delete_session(session.id)

    # Delete a branch
    delete_branch(session.id, branch.id)


except BranchedError as e:
    print(f"Error {e.code}: {e.detail}")
```

## Example Output from example_usage.py

When you run the example code, you'll see output similar to the following:

```
================================================================================
============================= INITIALIZING CLIENT ==============================
================================================================================
 Client initialized with base URL: https://branched-backend.onrender.com
Checking server health...
  Attempt 1/5: Server not ready yet - [500] The read operation timed out
Waiting 5.0 seconds before retry...
 Server is ready!

================================================================================
============================ CREATING A NEW SESSION ============================
================================================================================
 Created session: 71a9...dc95
Root node ID: bbf...e4a
Initial message: 'Hello, I'm testing the Branched SDK!'

================================================================================
============================== CREATING A BRANCH ===============================
================================================================================
 Created branch: 322...0d94
LLM Response: Sure, I'd be happy to help you explore the Branch SDK! The Branch SDK is a powerful tool for deep linking and attribution, often used in mobile apps to enhance user experience and track the effectiveness of marketing campaigns...

================================================================================
============================= GETTING SESSION INFO =============================
================================================================================
Session ID: 71a9...c95
Created at: 2025-06-05 22:39:44.639567
Number of nodes: 2

================================================================================
========================== GETTING MESSAGES IN BRANCH ==========================
================================================================================
Messages in branch 32278e03-dcbb-4c68-aaee-1ef237800d94:

================================================================================
============================= LISTING ALL SESSIONS =============================
================================================================================
Found 4 sessions:
  1. Session 71...c95 - Created: 2025-06-05 22:39:44.639567
  2. Session e3a...8ef54 - Created: 2025-06-01 05:01:09.895771
  3. Session 77...17 - Created: 2025-05-30 23:39:57.331853
  4. Session e78...d6eb - Created: 2025-05-27 23:02:38.419350

================================================================================
================================= CLEANING UP ==================================
================================================================================
 Deleted branch: 322...d94
 Deleted session: 71a...c95

================================================================================
============================== EXAMPLE COMPLETED! ==============================
================================================================================
```

## Available Methods

- `create_session(initial_message: str) -> ChatSessionRead`
- `create_branch(session_id: UUID, parent_id: UUID, user_message: str) -> TreeNodeRead`
- `get_session_info(session_id: UUID) -> ChatSessionRead`
- `get_session_messages(session_id: UUID, branch_id: UUID) -> List[TreeNodeRead]`
- `get_sessions() -> List[ChatSessionRead]`
- `delete_session(session_id: UUID) -> None`
- `delete_branch(session_id: UUID, branch_id: UUID) -> None`

## Error Handling

All API methods raise a `BranchedError` exception for any non-successful responses. The exception includes:

- `code`: HTTP status code
- `detail`: Error message from the server
