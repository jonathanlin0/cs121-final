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
            try:
                product_id = int(product_input)
            except ValueError:
                print("Invalid product ID. Please enter an integer.")
                continue
            # Validate product_id using value_exists
            if not DBUtils.value_exists(conn, "products", "product_id", product_id):
                print(f"Product with ID {product_id} does not exist. Please try again.")
                continue

            supplier_input = input("Enter supplier ID for this product: ").strip()
            try:
                supplier_id = int(supplier_input)
            except ValueError:
                print("Invalid supplier ID. Please enter an integer.")
                continue
            # Validate supplier_id using value_exists
            if not DBUtils.value_exists(conn, "suppliers", "supplier_id", supplier_id):
                print(f"Supplier with ID {supplier_id} does not exist. Please try again.")
                continue

            product_ids.append(product_id)
            supplier_ids.append(supplier_id)
        
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
        conn.rollback()
        print("Transaction rolled back due to error:", e)
    finally:
        cursor.close()

def admin_update_product(conn):
    # Loop until a valid, nonempty product_id is entered.
    while True:
        product_input = input("Enter Product ID to update: ").strip()
        if not product_input:
            print("Product ID cannot be empty. Please try again.")
            continue
        try:
            product_id = int(product_input)
        except ValueError:
            print("Invalid product ID. Please enter an integer.")
            continue
        if DBUtils.value_exists(conn, "products", "product_id", product_id):
            break
        else:
            print("No product found with the given Product ID. Please try again.")
    
    # Loop until a nonempty new product name is provided.
    while True:
        new_name = input("Enter new product name: ").strip()
        if new_name:
            break
        else:
            print("Product name cannot be empty. Please try again.")
    
    cursor = conn.cursor()
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
