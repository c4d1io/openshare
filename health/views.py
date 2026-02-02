from django.shortcuts import render

from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError


def health_check(request):
    db_status = "up"

    try:
        connections["default"].cursor()
    except OperationalError:
        db_status = "down"

    status = 200 if db_status == "up" else 503

    return JsonResponse(
        {
            "status": "Healthy" if status == 200 else "degraded",
            "database": db_status,
        },
        status=status,
    )

