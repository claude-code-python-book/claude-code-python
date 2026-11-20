class BillingResult(TypedDict):
    invoices: dict[str, dict[str, str | int]]
    customers: dict[str, dict[str, str | int]]
    errors: list[str]
    grand_total: str


def run_billing(
    rows: Iterable[Mapping[str, str]],
    today: date,
    report_dir: str | os.PathLike[str] | None = None,
) -> BillingResult:
