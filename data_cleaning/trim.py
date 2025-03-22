# removes arbitrary orders from the original dataset because it was too large

import pandas as pd

# Define file paths
file_path_orders = "data/orders.csv"
backup_path_orders = "data/orders_old1.csv"
file_path_products_in_order = "data/products_in_order.csv"
backup_path_products_in_order = "data/products_in_order_old1.csv"

# Read the orders CSV file
df_orders = pd.read_csv(file_path_orders)
print("Original orders shape:", df_orders.shape)

# Backup the original orders file
df_orders.to_csv(backup_path_orders, index=False)

# Filter out rows where user_id > 7000
df_orders_filtered = df_orders[df_orders['user_id'] <= 7000]
print("Filtered orders shape:", df_orders_filtered.shape)

# Save the filtered orders file
df_orders_filtered.to_csv(file_path_orders, index=False)

# Read the products_in_order CSV file
df_products_in_order = pd.read_csv(file_path_products_in_order)
print("Original products_in_order shape:", df_products_in_order.shape)

# Backup the original products_in_order file
df_products_in_order.to_csv(backup_path_products_in_order, index=False)

# Filter products_in_order to retain only orders present in the filtered orders file
valid_order_ids = set(df_orders_filtered['order_id'])
df_products_in_order_filtered = df_products_in_order[df_products_in_order['order_id'].isin(valid_order_ids)]
print("Filtered products_in_order shape:", df_products_in_order_filtered.shape)

# Save the filtered products_in_order file
df_products_in_order_filtered.to_csv(file_path_products_in_order, index=False)

print("Files processed successfully. Backups saved at:")
print("-", backup_path_orders)
print("-", backup_path_products_in_order)
