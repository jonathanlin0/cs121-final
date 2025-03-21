# app_admin.py
import sys
import json
from db_utils import DBUtils

# ----- Admin Functions (update/insert queries) -----

def admin_add_new_order(conn):
    cursor = conn.cursor()
    try:
        # Get basic order information and insert a new order
        user_id = input("Enter Customer ID: ")
        store_id = input("Enter Store ID: ")
        query = "INSERT INTO orders (user_id, order_timestamp, store_id) VALUES (%s, NOW(), %s)"
        cursor.execute(query, (user_id, store_id))
        order_id = cursor.lastrowid
        print(f"New order created with Order ID: {order_id}")
        
        # Continuously ask for product and supplier pairs.
        product_ids = []
        supplier_ids = []
        while True:
            product_input = input("Enter product ID (or press Enter to finish): ").strip()
            if product_input == "":
                break
            supplier_input = input("Enter supplier ID for this product: ").strip()
            product_ids.append(int(product_input))
            supplier_ids.append(int(supplier_input))
        
        if len(product_ids) == 0:
            print("No products were entered. Rolling back order creation.")
            conn.rollback()
            return
        
        # Convert lists to JSON strings.
        products_json = json.dumps(product_ids)
        suppliers_json = json.dumps(supplier_ids)
        
        # Call the stored procedure to insert the products for the order.
        call_query = "CALL add_new_order(%s, %s, %s)"
        cursor.execute(call_query, (order_id, products_json, suppliers_json))
        
        # Commit all changes together.
        conn.commit()
        print("Order and products inserted successfully within a single transaction.")
    except Exception as e:
        # Roll back any changes if an error occurs.
        conn.rollback()
        print("Transaction rolled back due to error:", e)
    finally:
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
    conn = DBUtils.get_conn("appadmin", "admin")
    if not conn:
        print("Failed to connect to the database.")
        sys.exit(1)

    print("Welcome to the Supermarket Admin Application")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    is_auth, is_admin = DBUtils.authenticate_user(conn, username, password)
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
