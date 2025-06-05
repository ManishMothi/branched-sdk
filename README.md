# branched-sdk

`pip install branched-sdk`

```python
from src.branched_sdk import BranchedClient, BranchedError

# Option 1: explicit
client = Branched(api_key="YOUR_KEY", base_url="https://api.branched.com")

# Option 2: use env var
# export Branched_API_KEY="YOUR_KEY"
client = BranchedClient()

# Create a session
try:
    session_id = client.create_session("My first chat")
    print("Session:", session_id)
except BranchedError as e:
    print("Error:", e.code, e.detail)
```
