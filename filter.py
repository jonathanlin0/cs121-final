import pandas as pd

# file paths
orders_file = "data/orders.csv"
products_file = "data/products.csv"
order_products_file = "data/order_products.csv"
aisles_file = "data/aisles.csv"
departments_file = "data/departments.csv"
filtered_output_file = order_products_file

# load relevant datasets
orders_df = pd.read_csv(orders_file)
products_df = pd.read_csv(products_file)
aisles_df = pd.read_csv(aisles_file)
departments_df = pd.read_csv(departments_file)
order_products_df = pd.read_csv(order_products_file)

# remove 'eval_set' column if it exists (not relevant for our use case)
if 'eval_set' in orders_df.columns:
    orders_df.drop(columns=['eval_set'], inplace=True)

initial_rows = len(products_df)
# ensure foreign key integrity for products.csv
products_df = products_df[
    products_df['aisle_id'].isin(aisles_df['aisle_id']) &
    products_df['department_id'].isin(departments_df['department_id'])
]
curr_rows = len(products_df)
print(f"Filtered out {initial_rows - curr_rows} rows in products.csv")


# initial row count
initial_rows = len(order_products_df)
print(f"Initial rows in order_products: {initial_rows}")

# filter order_products by valid order_id and product_id
filtered_order_products = order_products_df[
    order_products_df['order_id'].isin(orders_df['order_id']) &
    order_products_df['product_id'].isin(products_df['product_id'])
]

# compute filtered out rows
filtered_out_rows = initial_rows - len(filtered_order_products)
print(f"Rows filtered out: {filtered_out_rows}")

# final row count
final_rows = len(filtered_order_products)
print(f"Final rows after filtering: {final_rows}")

# save the filtered data (overwrite the old file)
filtered_order_products.to_csv(filtered_output_file, index=False)

print(f"Filtered data saved to {filtered_output_file}")

orders_df.to_csv(orders_file, index=False)