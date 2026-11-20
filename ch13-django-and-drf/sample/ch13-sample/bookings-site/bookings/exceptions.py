"""API errors that DRF turns into responses."""

from rest_framework import status
from rest_framework.exceptions import APIException


class Conflict(APIException):
    """409: the request clashes with the current state of the booking or room."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = "This room is already booked at that time."
    default_code = "conflict"
