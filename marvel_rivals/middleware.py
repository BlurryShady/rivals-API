"""Custom middleware for request observability."""

import logging
import threading
import uuid

_request_local = threading.local()


def _get_request_id():
    return getattr(_request_local, "request_id", "-")


class RequestIDFilter(logging.Filter):
    """Attach a request_id attribute to every log record."""

    def filter(self, record):
        record.request_id = _get_request_id()
        return True


class RequestIDMiddleware:
    """Ensure every request/response pair carries an X-Request-ID."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        _request_local.request_id = request_id
        request.request_id = request_id

        try:
            response = self.get_response(request)
        finally:
            if hasattr(_request_local, "request_id"):
                delattr(_request_local, "request_id")

        response["X-Request-ID"] = request_id
        return response
