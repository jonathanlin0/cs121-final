
import pandas as pd
from datetime import datetime

def verify_order_timestamps(csv_path):
    df = pd.read_csv(csv_path)
    
    df_sorted = df.sort_values(by=['user_id', 'customer_order_number'])
    
    
    # Assumes timestamps are in a SQL-friendly format such as "YYYY-MM-DD HH:MM:SS"
    df_sorted['order_timestamp'] = pd.to_datetime(df_sorted['order_timestamp'])
    
    errors_found = False
    
    for user, group in df_sorted.groupby('user_id'):
        # (Group is already sorted by customer_order_number)
        previous_timestamp = None
        for _, row in group.iterrows():
            current_timestamp = row['order_timestamp']
            if previous_timestamp is not None:
                # Check if the current order timestamp is not strictly after the previous one
                if current_timestamp <= previous_timestamp:
                    print(f"Data integrity error for user {user} on order {row['customer_order_number']}: "
                          f"current timestamp {current_timestamp} is not after previous timestamp {previous_timestamp}")
                    errors_found = True
            previous_timestamp = current_timestamp

    if not errors_found:
        print("Data integrity verified: All orders are in increasing timestamp order for each user.")
        
if __name__ == '__main__':
    csv_path = 'data/orders.csv'
    verify_order_timestamps(csv_path)
