# removes all orders with no occurances in products_in_order.csv
# remove all rows in products_in_order where the order_id doesn't appear in orders.csv

import pandas as pd

# Load the CSV files
orders = pd.read_csv('data/orders.csv')
products_in_order = pd.read_csv('data/products_in_order.csv')

# Filter orders to keep only those order_ids that appear in products_in_order
orders_filtered = orders[orders['order_id'].isin(products_in_order['order_id'])]

# Filter products_in_order to keep only those order_ids that appear in the filtered orders
products_in_order_filtered = products_in_order[products_in_order['order_id'].isin(orders_filtered['order_id'])]

# Optional: Save the filtered data to new CSV files
orders_filtered.to_csv('data/orders.csv', index=False)
products_in_order_filtered.to_csv('data/products_in_order.csv', index=False)

# Print a message indicating completion
print("Filtering complete. Filtered files saved as 'orders_filtered.csv' and 'products_in_order_filtered.csv'.")
