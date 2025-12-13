"""Simple health check endpoint for uptime monitoring."""

import os

from django.http import JsonResponse
from django.utils import timezone


def health_view(_request):
    return JsonResponse(
        {
            "status": "ok",
            "timestamp": timezone.now().isoformat(),
            "commit": os.environ.get("GIT_COMMIT", "local"),
        }
    )
