def discounted(net: Decimal, code: str) -> Decimal:
    if code == "SAVE10":
        net = net * Decimal("0.90")
    return net
