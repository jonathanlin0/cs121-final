import pandas as pd

file_path = "data/orders.csv"
backup_path = "data/orders_old.csv"

# Read the CSV file
df = pd.read_csv(file_path)
print(df.shape)

# Backup the original file
df.to_csv(backup_path, index=False)

# remove the last 100 rows
df_trimmed = df.iloc[:-400000]

# Save the trimmed file back to the original location
df_trimmed.to_csv(file_path, index=False)

df.to_csv(backup_path, index=False)

print("File processed successfully. Backup saved at:", backup_path)
