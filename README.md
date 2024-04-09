# DistributedLab
## Task 1: Orderbook

My solution is effective for relatively small list sizes corresponding to the order book. Since the sorting occurs using a built-in sort method written in C, it typically has a time complexity of O(n log n), where n is the number of orders in the corresponding list. However, since we sort after each insertion, the overall time complexity is greatly reduced since the list is nearly sorted most of the time.
However, if the list is expected to grow to 10,000 or more, further optimizations such as binary search trees or the use of parallel processing techniques may be required.
Spent about 3 hours

Exsample:

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

Answer:

    BalanceChange{'user_id': 1, 'value': -20, 'currency_string': 'UAH'}
    BalanceChange{'user_id': 1, 'value': 480, 'currency_string': 'USD'}

    BalanceChange{'user_id': 10, 'value': -480, 'currency_string': 'USD'}
    BalanceChange{'user_id': 10, 'value': 20, 'currency_string': 'UAH'}

    BalanceChange{'user_id': 2, 'value': -20, 'currency_string': 'UAH'}
    BalanceChange{'user_id': 2, 'value': 500, 'currency_string': 'USD'}

    BalanceChange{'user_id': 10, 'value': -500, 'currency_string': 'USD'}
    BalanceChange{'user_id': 10, 'value': 20, 'currency_string': 'UAH'}

## Task 2: Maze
Spent about 5 hours
I use the Depth First Search (DFS) algorithm because of its simplicity and effectiveness in creating complex and interesting mazes.
DFS has complexity O(n), where n is the number of cells in the maze. To improve the maze, I loop some sections.
To set the required number of traps and check the availability of the treasure, I use a path checking algorithm that uses breadth-first search (BFS), the time complexity of which is O (n).

![img.png](img.png)

## Task 3: Website analytics
Spent about 2 hours
The time complexity of this algorithm is O(n) 

