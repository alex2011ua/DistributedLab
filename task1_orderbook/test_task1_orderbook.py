from task1_orderbook import Order, Orderbook
from random import randint


def test_orderbook():
    """Verify that orderbook works as expected."""

    order_sell_1 = Order(1, 20, 24, True)
    order_sell_2 = Order(2, 40, 25, True)
    order_buy_3 = Order(10, 40, 25, False)

    orderbook = Orderbook()
    orderbook.add_order(order_sell_1)
    orderbook.add_order(order_sell_2)
    orderbook.add_order(order_buy_3)

    assert len(orderbook.buy_orders) == 1
    assert len(orderbook.sell_orders) == 2

    print(orderbook.balance_change())
    assert len(orderbook.buy_orders) == 0
    assert len(orderbook.sell_orders) == 1


def test_random_orders():
    """Test speed in creation a lot of random orders."""

    orderbook = Orderbook()
    iteration = 1000
    for i in range(10 * iteration):
        orderbook.add_order(Order(i, i, randint(50, 70), True))
        orderbook.add_order(Order(i, i, randint(50, 70), False))
    assert len(orderbook.sell_orders) == 10*iteration
    orderbook.balance_change()
    assert (4*iteration < (len(orderbook.sell_orders)) < 6*iteration)

