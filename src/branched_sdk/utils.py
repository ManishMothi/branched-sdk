from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import httpx

# Retry on any httpx.HTTPStatusError with 500–599, up to 3 attempts with exponential backoff.
def is_5xx(exc: Exception) -> bool:
    # httpx raises HTTPStatusError for non-2xx if you call .raise_for_status()
    if isinstance(exc, httpx.HTTPStatusError):
        return 500 <= exc.response.status_code < 600
    return False

retry_on_5xx = retry(
    retry=retry_if_exception_type(httpx.HTTPStatusError) & retry_if_exception_type(is_5xx),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(3),
)