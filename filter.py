import pandas as pd

# File paths
orders_file = "data/orders.csv"
products_file = "data/products.csv"
order_products_file = "data/order_products.csv"
filtered_output_file = order_products_file  # Overwrite the same file

# Load relevant datasets
orders_df = pd.read_csv(orders_file, usecols=['order_id'])
products_df = pd.read_csv(products_file, usecols=['product_id'])
order_products_df = pd.read_csv(order_products_file)

# Initial row count
initial_rows = len(order_products_df)
print(f"Initial rows in order_products: {initial_rows}")

# Filter order_products by valid order_id and product_id
filtered_order_products = order_products_df[
    order_products_df['order_id'].isin(orders_df['order_id']) &
    order_products_df['product_id'].isin(products_df['product_id'])
]

# Compute filtered out rows
filtered_out_rows = initial_rows - len(filtered_order_products)
print(f"Rows filtered out: {filtered_out_rows}")

# Final row count
final_rows = len(filtered_order_products)
print(f"Final rows after filtering: {final_rows}")

# Save the filtered data (overwrite the old file)
filtered_order_products.to_csv(filtered_output_file, index=False)

print(f"Filtered data saved to {filtered_output_file}")
