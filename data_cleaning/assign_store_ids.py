# adds store_id values to all the orders

import pandas as pd
import numpy as np

CSV_PATH = 'data/orders.csv'

df = pd.read_csv(CSV_PATH)

np.random.seed(42)

df['store_id'] = np.random.randint(1, 21, size=len(df))

df.to_csv(CSV_PATH, index=False)
