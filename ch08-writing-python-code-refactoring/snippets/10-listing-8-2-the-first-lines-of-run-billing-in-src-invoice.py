def run_billing(rows, today, report_dir=None):
    errors = []
    invoices = {}
    for i in range(len(rows)):
        row = rows[i]
        n = i + 2  # row 1 is the CSV header
        bad = False
        for f in ["invoice_id", "customer", "region", "sku", "qty", "unit_price"]:
            if f not in row.keys() or row[f] is None or row[f].strip() == "":
                errors.append("row " + str(n) + ": missing " + f)
                bad = True
                break
        if bad:
            continue
        try:
            qty = int(row["qty"])
        except ValueError:
            errors.append("row " + str(n) + ": qty is not a whole number")
            continue
        if qty <= 0:
            errors.append("row " + str(n) + ": qty must be positive")
            continue
