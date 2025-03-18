import pandas as pd

# file paths
orders_file = "data/orders.csv"
products_file = "data/products.csv"
products_in_order_file = "data/products_in_order.csv"
aisles_file = "data/aisles.csv"
departments_file = "data/departments.csv"
filtered_output_file = products_in_order_file

# load relevant datasets
orders_df = pd.read_csv(orders_file)
products_df = pd.read_csv(products_file)
aisles_df = pd.read_csv(aisles_file)
departments_df = pd.read_csv(departments_file)
products_in_order_df = pd.read_csv(products_in_order_file)

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
initial_rows = len(products_in_order_df)
print(f"Initial rows in products_in_order: {initial_rows}")

# filter products_in_order by valid order_id and product_id
filtered_products_in_order = products_in_order_df[
    products_in_order_df['order_id'].isin(orders_df['order_id']) &
    products_in_order_df['product_id'].isin(products_df['product_id'])
]

# compute filtered out rows
filtered_out_rows = initial_rows - len(filtered_products_in_order)
print(f"Rows filtered out: {filtered_out_rows}")

# final row count
final_rows = len(filtered_products_in_order)
print(f"Final rows after filtering: {final_rows}")

# save the filtered data (overwrite the old file)
filtered_products_in_order.to_csv(filtered_output_file, index=False)

print(f"Filtered data saved to {filtered_output_file}")

orders_df.to_csv(orders_file, index=False)