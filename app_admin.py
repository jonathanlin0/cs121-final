# app_admin.py
import sys
from db_utils import get_conn, authenticate_user

# ----- Admin Functions (update/insert queries) -----
def admin_add_new_order(conn):
    cursor = conn.cursor()
    
    # Get basic order information
    user_id = input("Enter Customer ID: ")
    store_id = input("Enter Store ID: ")
    query = "INSERT INTO orders (user_id, order_timestamp, store_id) VALUES (%s, NOW(), %s)"
    cursor.execute(query, (user_id, store_id))
    conn.commit()
    order_id = cursor.lastrowid
    print(f"New order created with Order ID: {order_id}")
    
    # Get the comma-separated product IDs, remove spaces, and split into a list
    products_str = input("Enter a comma separated list of product IDs: ")
    products_str = products_str.replace(" ", "")
    if not products_str:
        print("Error: No product IDs provided. Returning to main menu.")
        cursor.close()
        return
    
    product_ids = products_str.split(",")
    
    # Check if the list is empty (e.g., input was an empty string)
    if len(product_ids) == 0:
        print("Error: No product IDs provided. Returning to main menu.")
        cursor.close()
        return

    # Validate each product_id
    for pid in product_ids:
        query = "SELECT COUNT(*) FROM products WHERE product_id = %s"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        if result[0] == 0:
            print(f"Error: Product with product_id {pid} does not exist. Returning to main menu.")
            cursor.close()
            return

    # If all product IDs are valid, insert them into products_in_order
    for pid in product_ids:
        insert_query = "INSERT INTO products_in_order (order_id, product_id) VALUES (%s, %s)"
        cursor.execute(insert_query, (order_id, pid))
    conn.commit()
    print("Products added to order successfully.")
    
    cursor.close()

def admin_update_product(conn):
    cursor = conn.cursor()
    product_id = input("Enter Product ID to update: ")
    
    # Check if the product exists
    query = "SELECT COUNT(*) FROM products WHERE product_id = %s"
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()
    
    if result[0] == 0:
        print("No product found with the given Product ID.")
    else:
        new_name = input("Enter new product name: ")
        update_query = "UPDATE products SET product_name = %s WHERE product_id = %s"
        cursor.execute(update_query, (new_name, product_id))
        conn.commit()
        print("Product updated successfully.")
    
    cursor.close()

# ----- UI Helper -----
def show_admin_options():
    print("\nAdmin Options:")
    print("1 - Add a new order")
    print("2 - Update product name")
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
