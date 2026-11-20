"""Object-level permissions for bookings."""

from typing import Any

from rest_framework import permissions
from rest_framework.request import Request

from bookings.models import Booking


class IsOwnerOrStaff(permissions.BasePermission):
    """Allow a booking's owner and staff; everyone else is refused."""

    message = "You can only manage your own bookings."

    def has_object_permission(self, request: Request, view: Any, obj: Booking) -> bool:
        """Called by get_object(), so only for single-booking requests."""
        return bool(request.user.is_staff or obj.user_id == request.user.id)
