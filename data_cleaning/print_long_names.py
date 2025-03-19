import pandas as pd

# Load the CSV file
df = pd.read_csv('data/products.csv')

# Find rows where product_name length exceeds 255 characters
too_long = df[df['product_name'].str.len() > 255]

# Print out the row index and product_name that are being truncated
for index, row in too_long.iterrows():
    print(f"Row {index}: {row['product_name']}")
