# creates artificial datastamps for each order

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

orders = pd.read_csv('data/orders.csv')

# Dictionary to keep track of the last timestamp per user
last_timestamp_by_user = {}
timestamps = []

for i, row in orders.iterrows():
    user_id = row['user_id']
    target_hour = int(row['order_hour_of_day'])
    
    if user_id not in last_timestamp_by_user:
        # For the first order of a user, pick a random day in the first week of 2005.
        random_day = np.random.randint(1, 8)  # Day between 1 and 7 inclusive.
        base = datetime(2005, 1, random_day).replace(hour=target_hour, minute=0, second=0, microsecond=0)
        # Add a small amount of random noise (0-4 minutes and 0-4 seconds)
        noise_minutes = np.random.randint(0, 5)
        noise_seconds = np.random.randint(0, 5)
        candidate = base + timedelta(minutes=noise_minutes, seconds=noise_seconds)
    else:
        # For subsequent orders, add a random delay between 7 and 14 days (1-2 weeks)
        random_days = np.random.randint(7, 15)  # 7 to 14 days.
        prev_timestamp = last_timestamp_by_user[user_id]
        candidate = prev_timestamp + timedelta(days=random_days)
        # Adjust the candidate's hour to the current order's target hour.
        candidate = candidate.replace(hour=target_hour, minute=0, second=0, microsecond=0)
        # Optionally add a small amount of noise (0-4 minutes and 0-4 seconds)
        noise_minutes = np.random.randint(0, 5)
        noise_seconds = np.random.randint(0, 5)
        candidate = candidate + timedelta(minutes=noise_minutes, seconds=noise_seconds)
    
    last_timestamp_by_user[user_id] = candidate
    timestamps.append(candidate)

orders['order_timestamp'] = timestamps

# Save the orders CSV with the new timestamps.
orders.to_csv('data/orders.csv', index=False)
print("Updated orders.csv with new timestamps.")
