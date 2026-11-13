"""Verified HTTPS requests for optional literature sources."""
from __future__ import annotations
import json
import ssl
import urllib.error
import urllib.parse
import urllib.request

SSL_CONTEXT = ssl.create_default_context()

class MissingDependencyError(RuntimeError):
    """A selected adapter cannot parse results with its current dependencies."""

def require_html_parser():
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise MissingDependencyError("缺少可选依赖beautifulsoup4，网页结果无法解析；不等于零检索结果") from exc
    return BeautifulSoup

def get_text(url, params=None, headers=None, timeout=15, encoding="utf-8"):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    request_headers = {"User-Agent": "humanities-writing/1.0"}
    request_headers.update(headers or {})
    request = urllib.request.Request(url, headers=request_headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=SSL_CONTEXT) as response:
            return response.read().decode(encoding, errors="replace")
    except (urllib.error.URLError, TimeoutError, ssl.SSLError) as exc:
        # Do not echo URLs or credentials into logs or error strings.
        raise ConnectionError("Request failed; verify connectivity, certificate, or source configuration") from exc

def get_json(url, params=None, headers=None, timeout=15):
    return json.loads(get_text(url, params, headers, timeout))
