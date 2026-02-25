#!/usr/bin/env python3
"""
Fetch a landing page for ad campaign quality analysis.

Usage:
    python fetch_page.py https://example.com/landing
    python fetch_page.py https://example.com/landing --output page.html
"""

import argparse
import ipaddress
import socket
import sys
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install -r requirements.txt")
    sys.exit(1)


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ClaudeAds/1.1; +https://github.com/AgriciDaniel/claude-ads)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


def _is_public_ip(ip: ipaddress._BaseAddress) -> bool:
    return not (
        ip.is_private
        or ip.is_loopback
        or ip.is_reserved
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_unspecified
    )


def _is_public_host(hostname: str) -> tuple[bool, str]:
    if not hostname:
        return False, "Missing hostname"

    try:
        ip = ipaddress.ip_address(hostname)
        if not _is_public_ip(ip):
            return False, f"Blocked non-public IP: {hostname}"
        return True, ""
    except ValueError:
        pass

    try:
        addr_info = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as e:
        return False, f"DNS resolution failed for {hostname}: {e}"

    seen_ips: set[str] = set()
    for _, _, _, _, sockaddr in addr_info:
        ip_text = sockaddr[0]
        if ip_text in seen_ips:
            continue
        seen_ips.add(ip_text)

        try:
            ip = ipaddress.ip_address(ip_text)
        except ValueError:
            return False, f"Invalid resolved IP for {hostname}: {ip_text}"

        if not _is_public_ip(ip):
            return False, f"Blocked non-public IP for {hostname}: {ip_text}"

    return True, ""


def _validate_url(raw_url: str) -> tuple[str | None, str | None]:
    url = raw_url.strip()
    parsed = urlparse(url)

    if not parsed.scheme:
        url = f"https://{url}"
        parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return None, f"Invalid URL scheme: {parsed.scheme}"

    if not parsed.hostname:
        return None, "Invalid URL: missing hostname"

    is_public, reason = _is_public_host(parsed.hostname)
    if not is_public:
        return None, reason

    return url, None


def fetch_page(
    url: str,
    timeout: int = 30,
    follow_redirects: bool = True,
    max_redirects: int = 5,
) -> dict:
    """
    Fetch a landing page and return response details relevant to ad quality checks.

    Returns:
        Dictionary with url, status_code, content, headers, redirect_chain, error
    """
    result = {
        "url": url,
        "status_code": None,
        "content": None,
        "headers": {},
        "redirect_chain": [],
        "error": None,
    }

    validated_url, validation_error = _validate_url(url)
    if validation_error:
        result["error"] = validation_error
        return result

    try:
        session = requests.Session()
        session.max_redirects = max_redirects

        current_url = validated_url
        redirect_chain: list[str] = []

        for _ in range(max_redirects + 1):
            response = session.get(
                current_url,
                headers=DEFAULT_HEADERS,
                timeout=timeout,
                allow_redirects=False,
            )

            if not follow_redirects or not response.is_redirect:
                parsed_final = urlparse(response.url)
                if parsed_final.hostname:
                    is_public, reason = _is_public_host(parsed_final.hostname)
                    if not is_public:
                        result["error"] = f"Blocked final URL: {reason}"
                        return result

                result["url"] = response.url
                result["status_code"] = response.status_code
                result["content"] = response.text
                result["headers"] = dict(response.headers)
                result["redirect_chain"] = redirect_chain
                return result

            location = response.headers.get("Location")
            if not location:
                result["error"] = "Redirect response missing Location header"
                return result

            next_url = urljoin(current_url, location)
            parsed_next = urlparse(next_url)
            if parsed_next.scheme not in ("http", "https") or not parsed_next.hostname:
                result["error"] = f"Blocked redirect target: {next_url}"
                return result

            is_public, reason = _is_public_host(parsed_next.hostname)
            if not is_public:
                result["error"] = f"Blocked redirect target: {reason}"
                return result

            redirect_chain.append(next_url)
            current_url = next_url

        result["error"] = f"Too many redirects (max {max_redirects})"
        return result

    except requests.exceptions.Timeout:
        result["error"] = f"Request timed out after {timeout} seconds"
    except requests.exceptions.TooManyRedirects:
        result["error"] = f"Too many redirects (max {max_redirects})"
    except requests.exceptions.SSLError as e:
        result["error"] = f"SSL error: {e}"
    except requests.exceptions.ConnectionError as e:
        result["error"] = f"Connection error: {e}"
    except requests.exceptions.RequestException as e:
        result["error"] = f"Request failed: {e}"

    return result


def main():
    parser = argparse.ArgumentParser(description="Fetch a landing page for ad quality analysis")
    parser.add_argument("url", help="URL to fetch")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--timeout", "-t", type=int, default=30, help="Timeout in seconds")
    parser.add_argument("--no-redirects", action="store_true", help="Don't follow redirects")

    args = parser.parse_args()

    result = fetch_page(
        args.url,
        timeout=args.timeout,
        follow_redirects=not args.no_redirects,
    )

    if result["error"]:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result["content"])
        print(f"Saved to {args.output}")
    else:
        print(result["content"])

    print(f"\nURL: {result['url']}", file=sys.stderr)
    print(f"Status: {result['status_code']}", file=sys.stderr)
    if result["redirect_chain"]:
        print(f"Redirects: {' -> '.join(result['redirect_chain'])}", file=sys.stderr)


if __name__ == "__main__":
    main()
