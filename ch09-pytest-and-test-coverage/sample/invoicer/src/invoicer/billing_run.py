"""Deprecated: the billing run moved to `invoicer.billing`.

This module stays for code outside the repository, such as the finance
team's notebooks. Delete it once nothing imports it.
"""

import os
import warnings
from collections.abc import Iterable, Mapping
from datetime import date

from invoicer.billing import BillingResult, summarize_billing


def run_billing(
    rows: Iterable[Mapping[str, str]],
    today: date,
    report_dir: str | os.PathLike[str] | None = None,
) -> BillingResult:
    """Deprecated alias for `invoicer.billing.summarize_billing`."""
    warnings.warn(
        "invoicer.billing_run.run_billing is deprecated; "
        "use invoicer.billing.summarize_billing",
        DeprecationWarning,
        stacklevel=2,
    )
    return summarize_billing(rows, today, report_dir)
