def split_valid(cleaned: pd.DataFrame, month: str) -> Checked:
    """Validate every row; conflicting duplicate order IDs are all rejected."""
    clash = cleaned["order_id"].duplicated(keep=False)
    good: list[Order] = []
    bad: list[dict[str, str]] = []
    for position, row in enumerate(cleaned.to_dict("records")):
        if clash.iloc[position]:
            bad.append(
                {**row, "reason": "order_id: appears twice with different values"}
            )
            continue
        try:
            good.append(Order.model_validate(row, context={"month": month}))
        except ValidationError as error:
            bad.append({**row, "reason": _reason(error)})
    return Checked(
        _to_frame(good), pd.DataFrame(bad, columns=[*cleaned.columns, "reason"])
    )
