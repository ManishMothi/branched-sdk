# src/branched_sdk/errors.py
class BranchedError(Exception):
    """
    Wraps HTTP 4xx/5xx errors into a consistent exception type.
    """
    def __init__(self, code: int, detail: str):
        self.code = code
        self.detail = detail
        super().__init__(f"[{code}] {detail}")

    @classmethod
    def from_response(cls, status_code: int, message: str):
        return cls(status_code, message)

    @classmethod
    def from_exception(cls, exc: Exception):
        # Fallback if we can’t parse status/message from exc
        return cls(500, str(exc))
