    def get(self, customer_id: str, order_id: int) -> Order:
        """Return the customer's order.

        Raises:
            OrderNotFound: If the order does not exist or belongs to another
                customer. Both cases look the same, so ids can't be probed.
        """
        order = self._repo.get(order_id)
        if order is None or order.customer_id != customer_id:
            raise OrderNotFound(order_id)
        return order

    def _move(self, customer_id: str, order_id: int, target: OrderStatus) -> Order:
        order = self.get(customer_id, order_id)
        if target not in ALLOWED_MOVES[order.status]:
            raise InvalidTransition(order_id, order.status, target)
        order.status = target
        self._repo.save(order)
        return order
