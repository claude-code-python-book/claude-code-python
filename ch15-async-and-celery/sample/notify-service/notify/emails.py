"""The confirmation email itself: plain text, built from a Summary."""

from email.message import EmailMessage
from email.utils import make_msgid

from notify.summary import Summary

SENDER = "Shop <orders@shop.example>"


def confirmation_email(summary: Summary) -> EmailMessage:
    """Build the order confirmation email for one order."""
    order = summary.order
    lines = [f"Hello {order.name},", "", f"Thank you for order #{order.id}.", ""]
    for item, quantity, price in order.lines:
        lines.append(f"  {quantity} x {item:<24} {price * quantity:>9.2f}")
    lines += ["", f"  {'Total':<28} {order.total:>9.2f}", ""]
    if summary.delivery:
        lines.append(f"Expected delivery: {summary.delivery}.")
    else:
        lines.append("We'll email you a tracking link when your order ships.")
    if summary.points is not None:
        lines.append(f"Your loyalty balance is now {summary.points} points.")

    message = EmailMessage()
    message["From"] = SENDER
    message["To"] = order.email
    message["Subject"] = f"Your order #{order.id} is confirmed"
    message["Message-ID"] = make_msgid(idstring=f"order-{order.id}")
    message.set_content("\n".join(lines) + "\n")
    return message
