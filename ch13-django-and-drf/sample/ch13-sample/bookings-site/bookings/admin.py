"""The Django admin for rooms and bookings."""

from django.contrib import admin

from bookings.models import Booking, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Rooms: searchable, so bookings can autocomplete them."""

    list_display = ["name", "capacity", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Bookings, newest first, filterable by status and room."""

    list_display = ["room", "user", "start", "end", "attendees", "status"]
    list_filter = ["status", "room"]
    date_hierarchy = "start"
    search_fields = ["room__name", "user__username", "user__email"]
    autocomplete_fields = ["room", "user"]
    readonly_fields = ["created_at"]
    ordering = ["-start"]
