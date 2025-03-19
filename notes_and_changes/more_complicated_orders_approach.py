from faker import Faker
import random
from datetime import timedelta

fake = Faker()

def generate_orders(num_orders, day_of_week):
    """Generates a list of order dictionaries."""
    orders = []
    for _ in range(num_orders):
        order = {}
        order['shopping_cart_id'] = fake.uuid4()
        order['created_date'] = fake.date_time_between(start_date='-30d', end_date='now')

        if random.random() < 0.01:  # 1% chance of incomplete order
            order['completed_date'] = None
        else:
            completion_time = order['created_date'] + timedelta(minutes=random.randint(1, 10))
            order['completed_date'] = completion_time
        orders.append(order)
    return orders

def main():
    """Generates and prints orders based on the day of the week."""
    today = fake.date_time_between(start_date='-1d', end_date='now')
    day_of_week = today.weekday()  # 0 = Monday, 6 = Sunday

    if day_of_week == 6:  # Sunday
        num_orders = random.randint(10, 20)
    else:
        num_orders = random.randint(15, 40)

    orders = generate_orders(num_orders, day_of_week)

    for order in orders:
        print(order)

if __name__ == "__main__":
    main()