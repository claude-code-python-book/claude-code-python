from notify.emails import confirmation_email
from notify.summary import Summary
from tests.conftest import ORDER


def test_the_email_lists_lines_total_and_extras() -> None:
    message = confirmation_email(Summary(ORDER, "Thursday 19 November", 1320))
    body = message.get_content()
    assert message["To"] == "asha@example.com"
    assert message["Subject"] == "Your order #1042 is confirmed"
    assert "2 x Ceramic mug" in body and "24.50" in body
    assert "Total" in body and "68.50" in body
    assert "Expected delivery: Thursday 19 November." in body
    assert "1320 points" in body


def test_missing_extras_change_the_wording() -> None:
    body = confirmation_email(Summary(ORDER, None, None)).get_content()
    assert "tracking link" in body
    assert "points" not in body


def test_each_message_has_a_message_id() -> None:
    message = confirmation_email(Summary(ORDER, None, None))
    assert (
        message["Message-ID"].startswith("<") and "order-1042" in message["Message-ID"]
    )
