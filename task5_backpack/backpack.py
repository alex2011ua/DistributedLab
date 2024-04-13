import csv
import resource
import sys
from dataclasses import dataclass


@dataclass
class Transaction:
    tx_id: str
    tx_size: int
    tx_fee: int

    def __repr__(self):
        return self.tx_id


def read_transactions(file_path) -> list:
    transactions = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            tx_id, tx_size, tx_fee = row
            transactions.append((tx_id, int(tx_size), int(tx_fee)))
    return transactions


def construct_block(transactions):
    block = []
    block_size = 0
    total_fee = 0

    for i in range(len(transactions)):
        tx_id, tx_size, tx_fee = transactions[i]

        if block_size + tx_size <= 1048576:  # Block size limit (1MB)
            block.append(Transaction(tx_id, tx_size, tx_fee))
            block_size += tx_size
            total_fee += tx_fee

        else:
            if i != len(transactions) - 1:
                # sometimes instead of the last block it is better to insert the next two with a larger amount fit in
                if (
                    block_size - block[-1].tx_size <= transactions[i][1] + transactions[i + 1][1]
                    and block[-1].tx_fee < transactions[i][2] + transactions[i + 1][2]
                ):
                    # delete previous block
                    block.pop()
                    block_size -= block[-1].tx_size
                    total_fee -= block[-1].tx_fee
                    # insert next block
                    block.append(Transaction(tx_id, tx_size, tx_fee))
                    block_size += tx_size
                    total_fee += tx_fee

    return block, len(block), block_size, total_fee


def main(file_path):
    transactions = read_transactions(file_path)  # make list of all transactions
    sorted_transactions = sorted(
        transactions, key=lambda x: x[2] / x[1], reverse=True
    )  # sort list by relative_weight
    block, num_transactions, block_size, total_fee = construct_block(sorted_transactions)

    construction_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime
    print("Constructed Block:", block)
    print("Amount of transactions in the block:", num_transactions)
    print("The block size:", block_size)
    print("The total extracted value:", total_fee)
    print("Construction time:", construction_time)
    print("The max memory:", sys.getsizeof(transactions))


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
Construction time: 0.022948
The max memory: 184
"""
""" small
Amount of transactions in the block: 320
The block size: 1048117
The total extracted value: 227850
Construction time: 0.021096999999999998
The max memory: 85176
"""
""" standart
Amount of transactions in the block: 651
The block size: 1048437
The total extracted value: 508575
Construction time: 0.148719
The max memory: 800984
"""
"""big
Amount of transactions in the block: 895
The block size: 1047882
The total extracted value: 799948
Construction time: 1.5765289999999998
The max memory: 8448728
"""
"""super
Amount of transactions in the block: 1002
The block size: 1048122
The total extracted value: 963705
Construction time: 17.605584
The max memory: 89095160
"""
