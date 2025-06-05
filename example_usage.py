"""
Example usage of the Branched Python SDK.

This script demonstrates how to use the main features of the Branched SDK.
It includes retry logic and health checks to handle cold starts on free tier hosting.

Set up your environment first:
    export BRANCHED_API_KEY="your-api-key-here"
    export BRANCHED_BASE_URL="https://branched-backend.onrender.com"
"""

import os
import time
import sys
from uuid import UUID
from typing import Optional, Tuple
from dotenv import load_dotenv

# Import the Branched SDK
from branched_sdk import BranchedClient, BranchedError

def print_header(title: str):
    """Print a formatted section header."""
    print(f"\n{'=' * 80}")
    print(f" {title.upper()} ".center(80, '='))
    print(f"{'=' * 80}")

def print_success(message: str):
    """Print a success message."""
    print(f"✅ {message}")

def print_warning(message: str):
    """Print a warning message."""
    print(f"⚠️  {message}")

def print_error(message: str):
    """Print an error message."""
    print(f"❌ {message}", file=sys.stderr)

def wait_for_server(client: BranchedClient, max_retries: int = 5, initial_delay: float = 5.0) -> bool:
    """Wait for the server to be ready with exponential backoff."""
    print("Checking server health...")
    delay = initial_delay
    
    for attempt in range(1, max_retries + 1):
        try:
            health_response = client.health_check()
            print_success("Server is ready!")
            return True
        except BranchedError as e:
            print_warning(f"Attempt {attempt}/{max_retries}: Server not ready yet - {str(e)}")
        except Exception as e:
            print_warning(f"Attempt {attempt}/{max_retries}: Error checking server health - {str(e)}")
        
        if attempt < max_retries:
            print(f"Waiting {delay:.1f} seconds before retry...")
            time.sleep(delay)
            delay = min(delay * 2, 60)  # Exponential backoff with max 60s
    
    print_error("Server did not become ready in time. Please try again.")
    return False

def run_example():
    """Run the example usage of the Branched SDK."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Get API key from environment variables
    api_key = os.getenv("BRANCHED_API_KEY")
    base_url = os.getenv("BRANCHED_BASE_URL", "https://branched-backend.onrender.com")
    
    if not api_key:
        print_error("BRANCHED_API_KEY environment variable is not set.")
        print("Please set it before running this example:")
        print("  export BRANCHED_API_KEY='your-api-key-here'")
        return
    
    try:
        # Initialize the client with a longer timeout
        print_header("Initializing Client")
        client = BranchedClient(
            api_key=api_key, 
            base_url=base_url,
            timeout=60.0  # 60 second timeout
        )
        print_success(f"Client initialized with base URL: {base_url}")
        
        # Wait for server to be ready
        if not wait_for_server(client):
            return
        
        # Create a new session
        print_header("Creating a New Session")
        initial_message = "Hello, I'm testing the Branched SDK!"
        
        try:
            print("Creating a new session (this may take a few seconds for LLM inference)...")
            chat_session = client.create_session(initial_message)
            session_id = chat_session.id
            root_node = chat_session.nodes[0]
            print_success(f"✅ Created session: {session_id}")
            print(f"Root node ID: {root_node.id}")
            print(f"Initial message: '{initial_message}'")
            
            # Create a branch in the session
            print_header("Creating a Branch")
            branch_message = "Let's explore this branch"
            print(f"Creating a new branch (this may take a few seconds for LLM inference)...")
            branch = client.create_branch(
                session_id=session_id,
                parent_id=root_node.id,
                user_message=branch_message
            )
            print_success(f"✅ Created branch: {branch.id}")
            print(f"LLM Response: {branch.llm_response}")
            
            # Get session info
            print_header("Getting Session Info")
            session_info = client.get_session_info(session_id)
            print(f"Session ID: {session_info.id}")
            print(f"Created at: {session_info.created_at}")
            print(f"Number of nodes: {len(session_info.nodes)}")
            
            # Get messages in the branch
            print_header("Getting Messages in Branch")
            messages = client.get_session_messages(session_id, branch.id)
            print(f"Messages in branch {branch.id}:")
            for i, msg in enumerate(messages, 1):
                print(f"  {i}. {msg}")
            
            # List all sessions
            print_header("Listing All Sessions")
            sessions = client.get_sessions()
            print(f"Found {len(sessions)} sessions:")
            for i, session in enumerate(sessions, 1):
                print(f"  {i}. Session {session.id} - Created: {session.created_at}")
            
        except BranchedError as e:
            print_error(f"API Error: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
        except Exception as e:
            print_error(f"Unexpected error: {str(e)}")
        
        # Clean up (comment these out if you want to keep the session and branch)
        print_header("Cleaning Up")
        try:
            if 'branch' in locals():
                client.delete_branch(session_id, branch.id)
                print_success(f"Deleted branch: {branch.id}")
            
            if 'session_id' in locals():
                client.delete_session(session_id)
                print_success(f"Deleted session: {session_id}")
        except BranchedError as e:
            print_error(f"Error during cleanup: {e}")
        
        print_header("Example Completed!")
        
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    run_example()
