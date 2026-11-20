from django.http import HttpRequest, JsonResponse

from portal.models import Invoice


def invoice_list(request: HttpRequest) -> JsonResponse:
    rows = Invoice.objects.order_by("number").values("number", "customer")
    return JsonResponse({"invoices": list(rows)})
