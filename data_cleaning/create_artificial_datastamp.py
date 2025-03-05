# creates artificial datastamps

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

orders = pd.read_csv('data/orders.csv')

# Helper: Convert order_dow from dataset (assuming 0=Sunday, 1=Monday, …, 6=Saturday)
# to Python weekday() where Monday=0, Tuesday=1, …, Sunday=6.
def convert_order_dow(order_dow):
    return 6 if order_dow == 0 else order_dow - 1

# Helper: Given a previous timestamp, target weekday and target hour,
# return the earliest datetime strictly after prev_timestamp that has the given weekday and hour.
def next_timestamp(prev_timestamp, target_weekday, target_hour):
    # start a minute after the previous timestamp to ensure strictly increasing
    candidate = prev_timestamp + timedelta(minutes=1)
    # Replace time with the target hour (minutes, seconds zeroed)
    candidate = candidate.replace(hour=target_hour, minute=0, second=0, microsecond=0)
    # If that candidate is before or equal to prev_timestamp, push it one day ahead
    if candidate <= prev_timestamp:
        candidate += timedelta(days=1)
        candidate = candidate.replace(hour=target_hour, minute=0, second=0, microsecond=0)
    # Advance candidate until its weekday matches the target weekday.
    while candidate.weekday() != target_weekday:
        candidate += timedelta(days=1)
        candidate = candidate.replace(hour=target_hour, minute=0, second=0, microsecond=0)
    return candidate

timestamps = []

# For the first order, we force the timestamp to start at January 1, 2010,
# with the hour taken from the order_hour_of_day field.
first_row = orders.iloc[0]
target_hour_first = int(first_row['order_hour_of_day'])
base = datetime(2010, 1, 1).replace(hour=target_hour_first, minute=0, second=0, microsecond=0)
# Add a bit of random noise (minutes and seconds) for realism.
noise_minutes = np.random.randint(0, 60)
noise_seconds = np.random.randint(0, 60)
first_timestamp = base + timedelta(minutes=noise_minutes, seconds=noise_seconds)
timestamps.append(first_timestamp)

# For subsequent orders, generate a timestamp that is strictly after the previous one 
# and that matches the given order_dow and order_hour_of_day.
for i in range(1, len(orders)):
    row = orders.iloc[i]
    target_hour = int(row['order_hour_of_day'])
    # Convert the order_dow to Python weekday (0=Monday, …, 6=Sunday)
    target_weekday = convert_order_dow(int(row['order_dow']))
    
    prev_timestamp = timestamps[-1]
    candidate = next_timestamp(prev_timestamp, target_weekday, target_hour)
    
    noise_minutes = np.random.randint(0, 60)
    noise_seconds = np.random.randint(0, 60)
    # The candidate already has the correct hour; add noise without changing it.
    candidate = candidate + timedelta(minutes=noise_minutes, seconds=noise_seconds)
    
    timestamps.append(candidate)

orders['order_timestamp'] = timestamps

# The ISO-8601 format that pandas uses (e.g., "YYYY-MM-DD HH:MM:SS") is acceptable by SQL TIMESTAMP.
orders.to_csv('data/orders.csv', index=False)
