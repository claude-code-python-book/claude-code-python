from typing import Annotated, Any

from fastapi import APIRouter, Query, Response, status

from orders.deps import CurrentUser, OrderServiceDep
from orders.domain import OrderStatus
from orders.schemas import OrderCreate, OrderRead, Page, Problem

router = APIRouter(prefix="/orders", tags=["orders"])

NOT_FOUND: dict[int | str, dict[str, Any]] = {
    404: {"model": Problem, "description": "No such order for this customer"}
}
CONFLICT: dict[int | str, dict[str, Any]] = {
    409: {"model": Problem, "description": "The order's status does not allow it"}
}


@router.post("", status_code=status.HTTP_201_CREATED, summary="Place an order")
def place_order(
    data: OrderCreate, user: CurrentUser, service: OrderServiceDep, response: Response
) -> OrderRead:
    """Create a pending order for the signed-in customer."""
    order = service.place(user.customer_id, data)
    response.headers["Location"] = f"/orders/{order.id}"
    return OrderRead.model_validate(order)


@router.get("", summary="List your orders")
def list_orders(
    user: CurrentUser,
    service: OrderServiceDep,
    order_status: Annotated[OrderStatus | None, Query(alias="status")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Page[OrderRead]:
    """Return the customer's orders, newest first."""
    orders, count = service.page(user.customer_id, order_status, limit, offset)
    items = [OrderRead.model_validate(o) for o in orders]
    return Page[OrderRead](items=items, count=count, limit=limit, offset=offset)
