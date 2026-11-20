from fastapi import APIRouter, Depends

from orders.schemas import OrderRead
from orders.service import OrderService

router = APIRouter(prefix="/orders")


def get_service() -> OrderService: ...


@router.get("/{order_id}", response_model=OrderRead)
def get_order(id: int, service: OrderService = Depends(get_service)) -> OrderRead:
    ...
