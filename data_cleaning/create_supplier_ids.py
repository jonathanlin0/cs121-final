# assign a supplier_id to each row in products_in_order.csv

import pandas as pd
import random

# Step 1: Read orders.csv and create a mapping from order_id to store_id.
orders = pd.read_csv('data/orders.csv')
order_to_store = dict(zip(orders['order_id'], orders['store_id']))

# Step 2: Read stores.csv and create a mapping from store_id to city.
stores = pd.read_csv('data/stores.csv')
store_to_city = dict(zip(stores['store_id'], stores['city']))

# Step 3: Read suppliers.csv and group supplier_ids by city.
suppliers = pd.read_csv('data/suppliers.csv')
suppliers_by_city = {}
for _, row in suppliers.iterrows():
    city = row['city']
    supplier_id = row['supplier_id']
    suppliers_by_city.setdefault(city, []).append(supplier_id)

# Also create a complete list of supplier_ids (for fallback use).
all_supplier_ids = suppliers['supplier_id'].tolist()

# Step 4: Read products_in_order.csv and add supplier_id column.
products_in_order = pd.read_csv('data/products_in_order.csv')
supplier_ids = []  # list to hold the supplier_id for each row

for _, row in products_in_order.iterrows():
    order_id = row['order_id']
    store_id = order_to_store.get(order_id)
    # Get store's city if available; otherwise use None.
    store_city = store_to_city.get(store_id)
    
    # With 70% chance, pick a supplier in the same city.
    if random.random() < 0.7:
        if store_city and store_city in suppliers_by_city and suppliers_by_city[store_city]:
            chosen_supplier = random.choice(suppliers_by_city[store_city])
        else:
            # Fallback: if no supplier in the same city, choose from all.
            chosen_supplier = random.choice(all_supplier_ids)
    else:
        # 30% chance: pick a supplier not in the store's city.
        non_matching_suppliers = []
        for city, supp_ids in suppliers_by_city.items():
            if city != store_city:
                non_matching_suppliers.extend(supp_ids)
        if non_matching_suppliers:
            chosen_supplier = random.choice(non_matching_suppliers)
        else:
            # Fallback: if no supplier is outside the store's city, pick any supplier.
            chosen_supplier = random.choice(all_supplier_ids)
    
    supplier_ids.append(chosen_supplier)

# Add the supplier_id column to the products_in_order DataFrame.
products_in_order['supplier_id'] = supplier_ids

# Step 5: Save the updated products_in_order DataFrame to a new CSV file.
products_in_order.to_csv('data/products_in_order_with_suppliers.csv', index=False)
print("Updated products_in_order.csv saved as 'data/products_in_order_with_suppliers.csv'.")
