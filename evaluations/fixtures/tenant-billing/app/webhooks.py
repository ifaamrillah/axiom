"""Outbound webhooks and inbound signature checks."""

import hashlib
import hmac
import urllib.request


def sign(secret, body):
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


def verify_signature(secret, body, signature):
    return sign(secret, body) == signature


def send_test_webhook(url, payload):
    if not url.startswith("http"):
        raise ValueError("url must be http(s)")
    request = urllib.request.Request(url, data=payload, method="POST")
    with urllib.request.urlopen(request, timeout=5) as response:
        return response.status, response.read(2048)
