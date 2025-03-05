# app_admin.py
import sys
from db_utils import get_conn, authenticate_user

# ----- Admin Functions (update/insert queries) -----
def admin_add_new_order(conn):
    cursor = conn.cursor()
    user_id = input("Enter Customer ID: ")
    store_id = input("Enter Store ID: ")
    query = "INSERT INTO orders (user_id, order_timestamp, store_id) VALUES (%s, NOW(), %s)"
    cursor.execute(query, (user_id, store_id))
    conn.commit()
    print(f"New order created with Order ID: {cursor.lastrowid}")
    cursor.close()

def admin_update_product(conn):
    cursor = conn.cursor()
    product_id = input("Enter Product ID to update: ")
    new_name = input("Enter new product name: ")
    query = "UPDATE products SET product_name = %s WHERE product_id = %s"
    cursor.execute(query, (new_name, product_id))
    conn.commit()
    print("Product updated successfully.")
    cursor.close()

# ----- UI Helper -----
def show_admin_options():
    print("\nAdmin Options:")
    print("1 - Add a new order")
    print("2 - Update product details")
    print("q - Quit")
    return input("Enter an option: ").lower().strip()

def quit_ui():
    print("Goodbye!")
    sys.exit(0)

# ----- Main Application Flow for Admin -----
def main():
    # Connect using the admin account
    conn = get_conn("appadmin", "admin")
    if not conn:
        print("Failed to connect to the database.")
        sys.exit(1)

    print("Welcome to the Supermarket Admin Application")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    is_auth, is_admin = authenticate_user(conn, username, password)
    if not is_auth:
        print("Authentication failed. Please check your credentials.")
        sys.exit(1)
    if not is_admin:
        print("This application is for admin users only.")
        sys.exit(1)
    print(f"Welcome, {username}!")

    # Main loop for admin operations
    while True:
        option = show_admin_options()
        if option == "1":
            admin_add_new_order(conn)
        elif option == "2":
            admin_update_product(conn)
        elif option == "q":
            quit_ui()
        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    main()
