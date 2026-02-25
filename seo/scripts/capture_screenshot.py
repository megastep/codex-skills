#!/usr/bin/env python3
"""
Capture screenshots of web pages using Playwright.

Usage:
    python capture_screenshot.py https://example.com
    python capture_screenshot.py https://example.com --mobile
    python capture_screenshot.py https://example.com --output screenshots/
"""

import argparse
import ipaddress
import os
import socket
import sys
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("Error: playwright required. Install with: pip install playwright && playwright install chromium")
    sys.exit(1)


VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "laptop": {"width": 1366, "height": 768},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 812},
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


def capture_screenshot(
    url: str,
    output_path: str,
    viewport: str = "desktop",
    full_page: bool = False,
    timeout: int = 30000,
) -> dict:
    """
    Capture a screenshot of a web page.
    """
    result = {
        "url": url,
        "output": output_path,
        "viewport": viewport,
        "success": False,
        "error": None,
    }

    if viewport not in VIEWPORTS:
        result["error"] = f"Invalid viewport: {viewport}. Choose from: {list(VIEWPORTS.keys())}"
        return result

    validated_url, validation_error = _validate_url(url)
    if validation_error:
        result["error"] = validation_error
        return result

    vp = VIEWPORTS[viewport]

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": vp["width"], "height": vp["height"]},
                device_scale_factor=2 if viewport == "mobile" else 1,
            )
            page = context.new_page()

            # Block requests to non-http(s) or non-public hosts.
            host_cache: dict[str, tuple[bool, str]] = {}

            def route_handler(route):
                req_url = route.request.url
                parsed_req = urlparse(req_url)

                if parsed_req.scheme in ("data", "blob", "about"):
                    route.continue_()
                    return

                if parsed_req.scheme not in ("http", "https") or not parsed_req.hostname:
                    route.abort()
                    return

                cached = host_cache.get(parsed_req.hostname)
                if cached is None:
                    cached = _is_public_host(parsed_req.hostname)
                    host_cache[parsed_req.hostname] = cached

                if not cached[0]:
                    route.abort()
                    return

                route.continue_()

            page.route("**/*", route_handler)

            # Navigate and wait for network idle
            page.goto(validated_url, wait_until="networkidle", timeout=timeout)

            # Validate final URL after redirects
            parsed_final = urlparse(page.url)
            if parsed_final.scheme not in ("http", "https") or not parsed_final.hostname:
                browser.close()
                result["error"] = f"Blocked final URL: {page.url}"
                return result

            is_public, reason = _is_public_host(parsed_final.hostname)
            if not is_public:
                browser.close()
                result["error"] = f"Blocked final URL: {reason}"
                return result

            # Wait a bit more for any lazy-loaded content
            page.wait_for_timeout(1000)

            # Capture screenshot
            page.screenshot(path=output_path, full_page=full_page)

            result["success"] = True
            browser.close()

    except PlaywrightTimeout:
        result["error"] = f"Page load timed out after {timeout}ms"
    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(description="Capture web page screenshots")
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("--output", "-o", default="screenshots", help="Output directory")
    parser.add_argument("--viewport", "-v", default="desktop", choices=VIEWPORTS.keys())
    parser.add_argument("--all", "-a", action="store_true", help="Capture all viewports")
    parser.add_argument("--full", "-f", action="store_true", help="Capture full page")
    parser.add_argument("--timeout", "-t", type=int, default=30000, help="Timeout in ms")

    args = parser.parse_args()

    # Sanitize output path — prevent directory traversal
    output_dir = os.path.realpath(args.output)
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    if not (output_dir.startswith(cwd) or output_dir.startswith(home)):
        print("Error: Output path must be within current directory or home directory", file=sys.stderr)
        sys.exit(1)

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Generate filename from URL
    parsed = urlparse(args.url)
    base_name = parsed.netloc.replace(".", "_") if parsed.netloc else "page"

    viewports = VIEWPORTS.keys() if args.all else [args.viewport]

    for viewport in viewports:
        filename = f"{base_name}_{viewport}.png"
        output_path = os.path.join(args.output, filename)

        print(f"Capturing {viewport} screenshot...")
        result = capture_screenshot(
            args.url,
            output_path,
            viewport=viewport,
            full_page=args.full,
            timeout=args.timeout,
        )

        if result["success"]:
            print(f"  ✓ Saved to {output_path}")
        else:
            print(f"  ✗ Failed: {result['error']}")


if __name__ == "__main__":
    main()
