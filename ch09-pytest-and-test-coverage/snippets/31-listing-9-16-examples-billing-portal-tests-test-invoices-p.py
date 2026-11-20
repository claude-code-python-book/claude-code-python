from collections.abc import Callable
from datetime import date
from decimal import Decimal

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django import DjangoAssertNumQueries

from portal.models import Invoice

pytestmark = pytest.mark.django_db


@pytest.fixture
def make_invoice() -> Callable[..., Invoice]:
    def _make(number: str = "INV-1", **fields: object) -> Invoice:
        defaults = {
            "customer": "Acme Ltd",
            "gross": Decimal("100.00"),
            "issued": date(2026, 10, 1),
        }
        return Invoice.objects.create(number=number, **{**defaults, **fields})

    return _make


def test_fee_on_an_overdue_invoice(make_invoice: Callable[..., Invoice]) -> None:
    invoice = make_invoice()
    assert invoice.fee_on(date(2026, 11, 15)) == Decimal("1.50")


def test_no_fee_once_paid(make_invoice: Callable[..., Invoice]) -> None:
    invoice = make_invoice(paid=date(2026, 10, 20))
    assert invoice.fee_on(date(2026, 11, 15)) == Decimal("0.00")


def test_invoice_list_is_one_query(
    client: Client,
    make_invoice: Callable[..., Invoice],
    django_assert_num_queries: DjangoAssertNumQueries,
) -> None:
    make_invoice("INV-2")
    make_invoice("INV-1")
    with django_assert_num_queries(1):
        response = client.get(reverse("invoice-list"))
    numbers = [row["number"] for row in response.json()["invoices"]]
    assert numbers == ["INV-1", "INV-2"]


def test_admin_lists_invoices(admin_client: Client) -> None:
    response = admin_client.get("/admin/portal/invoice/")
    assert response.status_code == 200
