import requests
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)

API_URL = ""

@retry(
    retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError)),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def _post_invoice(payload: dict) -> dict:
    response = requests.post(API_URL, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

def submit_invoice(invoice) -> tuple[bool, str]:
    payload = invoice.model_dump(mode="json")

    try:
        result = _post_invoice(payload)
        logger.info(f"Successfully submitted {invoice.invoice_number}")
        return True, "ok"
    except requests.HTTPError as e:
        msg = f"HTTP error {e.response.status_code} for {invoice.invoice_number}: {e}"
        logger.error(msg)
        return False, msg
    except (requests.Timeout, requests.ConnectionError) as e:
        msg = f"Network error for {invoice.invoice_number} after retries: {e}"
        logger.error(msg)
        return False, msg