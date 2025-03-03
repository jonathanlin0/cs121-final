import pandas as pd

# Define file paths
file_path_orders = "data/orders.csv"
backup_path_orders = "data/orders_old1.csv"
file_path_order_products = "data/order_products.csv"
backup_path_order_products = "data/order_products_old1.csv"

# Read the orders CSV file
df_orders = pd.read_csv(file_path_orders)
print("Original orders shape:", df_orders.shape)

# Backup the original orders file
df_orders.to_csv(backup_path_orders, index=False)

# Filter out rows where user_id > 200
df_orders_filtered = df_orders[df_orders['user_id'] <= 10]
print("Filtered orders shape:", df_orders_filtered.shape)

# Save the filtered orders file
df_orders_filtered.to_csv(file_path_orders, index=False)

# Read the order_products CSV file
df_order_products = pd.read_csv(file_path_order_products)
print("Original order_products shape:", df_order_products.shape)

# Backup the original order_products file
df_order_products.to_csv(backup_path_order_products, index=False)

# Filter order_products to retain only orders present in the filtered orders file
valid_order_ids = set(df_orders_filtered['order_id'])
df_order_products_filtered = df_order_products[df_order_products['order_id'].isin(valid_order_ids)]
print("Filtered order_products shape:", df_order_products_filtered.shape)

# Save the filtered order_products file
df_order_products_filtered.to_csv(file_path_order_products, index=False)

print("Files processed successfully. Backups saved at:")
print("-", backup_path_orders)
print("-", backup_path_order_products)
