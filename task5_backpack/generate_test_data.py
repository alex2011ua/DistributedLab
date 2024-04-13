import csv
import random


def generate_test_data(file_path, num_transactions):
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["tx_id", "tx_size", "tx_fee"])  # Header
        for i in range(num_transactions):
            tx_id = f"tx{i}"
            tx_size = random.randint(1000, 100000)  # Random size
            tx_fee = random.randint(100, 1000)  # Random fee
            writer.writerow([tx_id, tx_size, tx_fee])


def main():
    file_path = "transactions_little.csv"
    num_transactions = 10
    generate_test_data(file_path, num_transactions)


if __name__ == "__main__":
    main()
