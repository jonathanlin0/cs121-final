import pandas as pd

store_ids = list(range(1, 21))

cities = [
    "Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno",
    "Sacramento", "Long Beach", "Oakland", "Bakersfield", "Anaheim",
    "Santa Ana", "Riverside", "Stockton", "Chula Vista", "Irvine",
    "Fremont", "San Bernardino", "Modesto", "Oxnard", "Fontana"
]

states = ["CA"] * len(cities)

df = pd.DataFrame({
    "store_id": store_ids,
    "city": cities,
    "state": states
})

df.to_csv("data/stores.csv", index=False)
