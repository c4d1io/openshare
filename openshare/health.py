from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError


def health_check(request):
    """Simple health-check endpoint.

    Returns JSON indicating overall status and whether the DB is reachable.
    """
    try:
        # Try obtaining a cursor; this will raise if DB is unavailable
        connections['default'].cursor()
        db_status = "up"
        status = "Healthy"
        code = 200
    except OperationalError:
        db_status = "down"
        status = "Unhealthy"
        code = 503

    payload = {"status": status, "database": db_status}
    return JsonResponse(payload, status=code)
