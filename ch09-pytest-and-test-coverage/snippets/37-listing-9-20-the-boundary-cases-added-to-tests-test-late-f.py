        pytest.param(31, "1.50", id="first-overdue-day"),
        pytest.param(59, "1.50", id="last-day-of-first-period"),
        pytest.param(
            60,
            "1.50",
            id="day-60",
            marks=pytest.mark.xfail(
                strict=True, reason="docstring says one period at day 60; code: two"
            ),
        ),
        pytest.param(61, "3.00", id="second-period"),
        pytest.param(209, "9.00", id="six-periods-below-cap"),
        pytest.param(210, "10.00", id="seventh-period-hits-cap"),
        pytest.param(3650, "10.00", id="capped"),
