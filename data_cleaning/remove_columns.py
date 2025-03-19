# remove columns from a given csv file

import pandas as pd

# Read the CSV file
df = pd.read_csv('data/orders.csv')

# Remove the specified columns
df.drop(columns=["customer_order_number" , "order_dow", "order_hour_of_day", "days_since_prior_order"], inplace=True)

# Write the updated DataFrame back to the same CSV file
df.to_csv('data/orders.csv', index=False)
