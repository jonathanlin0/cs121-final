CSV_PATH = 'data/orders.csv'
COLUMN = 'customer_order_number'

import pandas as pd

df = pd.read_csv(CSV_PATH)

df = df.drop(columns=[COLUMN])

df.to_csv(CSV_PATH, index=False)
