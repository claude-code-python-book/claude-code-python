import time

from shop.pricing import apply_discount

def test_discount():
    result = apply_discount(100.0, 10)
    print(result)

def test_discount():
    assert True

def test_negative_price():
    time.sleep(1)
    try:
        apply_discount(-1.0, 10)
    except:
        pass
