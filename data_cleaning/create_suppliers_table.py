# create the suppliers.csv file/data table

import pandas as pd
import random

# List of cities
cities = [
    "Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno",
    "Sacramento", "Long Beach", "Oakland", "Bakersfield", "Anaheim",
    "Santa Ana", "Riverside", "Stockton", "Chula Vista", "Irvine",
    "Fremont", "San Bernardino", "Modesto", "Oxnard", "Fontana"
]

# Initialize list to hold supplier records
suppliers = []

# Generate suppliers for each city
for city in cities:
    # Generate a random count between 3 and 6
    num_suppliers = random.randint(3, 6)
    for _ in range(num_suppliers):
        supplier_id = random.randint(10000, 99999)
        suppliers.append({
            "supplier_id": supplier_id,
            "city": city,
            "state": "CA"
        })

# Create DataFrame and save to CSV
df_suppliers = pd.DataFrame(suppliers)
df_suppliers.to_csv("data/suppliers.csv", index=False)

print("Created suppliers.csv with", df_suppliers.shape[0], "suppliers.")
