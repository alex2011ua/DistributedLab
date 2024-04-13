#!/usr/bin/env python3
import csv


def user_analytics(first_day_file: str, second_day_file: str) -> set:
    first_day = {}  # dict with all users, visited in first day
    unique_users = set()  # users, on the second day visited the page that hadn’t been visited on the first day


    with open(first_day_file) as csvfile:
        reader = csv.reader(csvfile)
        _headers = next(reader)
        for user_id, product_id, timestamp in reader:
            if user_id in first_day:
                first_day[user_id].add(product_id)
            else:
                first_day[user_id] = {product_id}

    with open(second_day_file) as csvfile:
        reader = csv.reader(csvfile)
        _headers = next(reader)
        for user_id, product_id, timestamp in reader:
            if user_id in first_day:
                if product_id not in first_day[user_id]:
                    unique_users.add(user_id)

    return unique_users


if __name__ == "__main__":
    users = user_analytics("2024-04-09.csv", "2024-04-10.csv")
    print(*users)
