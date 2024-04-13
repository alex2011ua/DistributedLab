import csv
import resource
import sys
from dataclasses import dataclass


@dataclass
class Transaction:
    tx_id: str
    tx_size: int
    tx_fee: int
    relative_weight: float

    def __repr__(self):
        return self.tx_id

    def __ge__(self, other):
        return self.relative_weight >= other.relative_weight

    def __gt__(self, other):
        return self.relative_weight > other.relative_weight

    def __le__(self, other):
        return self.relative_weight <= other.relative_weight

    def __lt__(self, other):
        return self.relative_weight < other.relative_weight


class Node:
    min_relative_weight = 0
    count = 0

    def __init__(self, data: Transaction | None = None):
        self.left = None
        self.right = None
        self.data = data
        Node.min_relative_weight = Node.min_relative_weight

    def find_min_node(self):
        current = self
        while current.left:
            current = current.left
        return current

    def delete_min_node(self):
        min_node: Node = self.find_min_node()

        if min_node.left is None and min_node.right is None:
            parent = self.find_parent(min_node)
            if parent:
                if parent.left == min_node:
                    parent.left = None
                else:
                    parent.right = None
        # If the minimum node has a subtree with equal values
        elif min_node.right:
            parent = self.find_parent(min_node)
            if parent:
                if parent.left == min_node:
                    parent.left = min_node.right
                else:
                    parent.right = min_node.right
            else:
                self.data = min_node.right.data
                self.left = min_node.right.left
                self.right = min_node.right.right
        Node.min_relative_weight = min_node.data.relative_weight
        Node.count -= 1

    def find_parent(self, node):
        parent = None
        current = self
        while current:
            if current == node:
                return parent
            elif node.data <= current.data:
                parent = current
                current = current.left
            else:
                parent = current
                current = current.right
        return None

    def insert(self, data: Transaction):
        # Compare the new value with the parent node
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                    Node.count += 1
                else:
                    self.left.insert(data)
            else:
                if self.right is None:
                    self.right = Node(data)
                    Node.count += 1
                else:
                    self.right.insert(data)
        else:
            self.data = data
            Node.count += 1

    def reverse_inorder_traversal_generator(self):
        """Return generator to pass through wood, starting with the highest relative_weight results."""

        if self.right:
            yield from self.right.reverse_inorder_traversal_generator()
        yield self.data
        if self.left:
            yield from self.left.reverse_inorder_traversal_generator()


def read_transactions(file_path) -> Node:
    """Read transactions from csv file and return a root node of pull transactions."""
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        pool_of_block: Node = Node()
        for row in reader:
            if Node.count < 2000:  # limit of size pull
                tx_id, tx_size, tx_fee = row
                relative_weight = int(tx_fee) / int(tx_size)
                transaction = Transaction(tx_id, int(tx_size), int(tx_fee), relative_weight)
                pool_of_block.insert(transaction)
            else:
                tx_id, tx_size, tx_fee = row
                relative_weight = int(tx_fee) / int(tx_size)
                if relative_weight > Node.min_relative_weight:  # if transaction better than in pool
                    transaction = Transaction(tx_id, int(tx_size), int(tx_fee), relative_weight)
                    pool_of_block.insert(transaction)  # add this transaction
                    pool_of_block.delete_min_node()  # remove the worst transaction from the pool
    return pool_of_block


def construct_block(transactions: Node):
    """Construct block from pool of transactions."""

    block = []
    block_size = 0
    total_fee = 0
    for transaction in transactions.reverse_inorder_traversal_generator():
        if block_size + transaction.tx_size <= 1048576:  # Block size limit (1MB)
            block.append(transaction)
            block_size += transaction.tx_size
            total_fee += transaction.tx_fee
    return block, len(block), block_size, total_fee


def main(file_path):
    transactions = read_transactions(file_path)
    block, num_transactions, block_size, total_fee = construct_block(transactions)

    construction_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime
    print("Constructed Block:", block)
    print("Amount of transactions in the block:", num_transactions)
    print("The block size:", block_size)
    print("The total extracted value:", total_fee)
    print("Construction time:", construction_time)
    max_memory_used = sys.getsizeof(list(transactions.reverse_inorder_traversal_generator()))
    print("The max memory:", max_memory_used)


if __name__ == "__main__":
    # print("little")
    # main('transactions_little.csv')
    # print("small")
    # main('transactions_small.csv')
    print("transactions")
    main("transactions.csv")
    # print("big")
    # main('transactions_big.csv')
    # print("super")
    # main('transactions_super.csv')

""" little
Amount of transactions in the block: 10
The block size: 645995
The total extracted value: 6599
Construction time: 0.024106
The max memory: 184
"""

""" small
Amount of transactions in the block: 320
The block size: 1048117
The total extracted value: 227850
Construction time: 0.047392
The max memory: 8856
"""
""" standart
Amount of transactions in the block: 651
The block size: 1048437
The total extracted value: 508575
Construction time: 0.10897899999999999
The max memory: 8856
"""
""" big
Amount of transactions in the block: 895
The block size: 1047756
The total extracted value: 799444
Construction time: 0.5807749999999999
The max memory: 8856
"""
""" super
Amount of transactions in the block: 1001
The block size: 1046990
The total extracted value: 962709
Construction time: 4.944677
The max memory: 8856
"""
