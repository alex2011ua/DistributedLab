class BalanceChange:
    def __init__(self, user_id: int, value: int, currency_string: str):
        self.user_id = user_id
        self.value = value
        self.currency_string = currency_string

    def __repr__(self):
        return type(self).__name__ + str(self.__dict__)


class Orderbook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.side:
            self.sell_orders.append(order)
            self.sell_orders.sort(key=lambda o: o.price)
        else:
            self.buy_orders.append(order)
            self.buy_orders.sort(key=lambda o: o.price, reverse=True)

    def balance_change(self) -> list[BalanceChange]:
        balance_change = []
        while self.buy_orders and self.sell_orders:
            sell: Order = self.sell_orders[0]
            buy: Order = self.buy_orders[0]

            if sell.price <= buy.price:  # making transaction
                amount: int = min(sell.amount, buy.amount)

                balance_change.append(BalanceChange(sell.user_id, -amount, "UAH"))
                balance_change.append(BalanceChange(sell.user_id, amount * sell.price, "USD"))
                sell.amount -= amount
                if sell.amount == 0:
                    self.sell_orders.remove(sell)

                balance_change.append(BalanceChange(buy.user_id, -(amount * sell.price), "USD"))
                balance_change.append(BalanceChange(buy.user_id, amount, "UAH"))
                buy.amount -= amount
                if buy.amount == 0:
                    self.buy_orders.remove(buy)
            else:
                break
        return balance_change


class Order:
    def __init__(self, user_id: int, amount: int, price: int, side: bool):
        self.user_id = user_id
        self.amount = amount
        self.price = price
        self.side = side


if __name__ == "__main__":

    order_book = Orderbook()

    # sell
    order_book.add_order(Order(1, 20, 24, True))
    order_book.add_order(Order(2, 40, 25, True))
    order_book.add_order(Order(3, 40, 26, True))

    # buy
    order_book.add_order(Order(10, 40, 25, False))
    order_book.add_order(Order(11, 40, 24, False))
    order_book.add_order(Order(12, 40, 23, False))

    # Match orders
    print(*order_book.balance_change(), sep="\n")
