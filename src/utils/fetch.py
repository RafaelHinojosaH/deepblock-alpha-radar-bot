import os
from typing import Any, Dict, Optional

import requests
from .logger import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT = 10

def get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> Optional[Dict[str, Any]]:
    proxies = {}
    http_proxy = os.getenv("HTTP_PROXY", "")
    https_proxy = os.getenv("HTTPS_PROXY", "")

    if http_proxy:
        proxies["http"] = http_proxy
    if https_proxy:
        proxies["https"] = https_proxy

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=timeout, proxies=proxies)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

