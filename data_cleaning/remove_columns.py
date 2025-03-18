import pandas as pd

# Read the CSV file
df = pd.read_csv('data/products_in_order.csv')

# Remove the specified columns
df.drop(columns=["add_to_cart_order" , "reordered"], inplace=True)

# Write the updated DataFrame back to the same CSV file
df.to_csv('data/products_in_order.csv', index=False)
