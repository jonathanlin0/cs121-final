# app_client.py
import sys
from db_utils import DBUtils

# ----- Client Functions (read-only queries) -----
def client_view_store_efficiency(conn):
    cursor = conn.cursor()
    query = """
    SELECT 
        s.store_id, 
        s.city, 
        store_efficiency(s.store_id) AS supplier_efficiency, 
        (
            SELECT COUNT(*) 
            FROM products_in_order p
            NATURAL JOIN orders o
            WHERE o.store_id = s.store_id
        ) AS num_purchased_products
    FROM stores s
    ORDER BY supplier_efficiency DESC, num_purchased_products DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\nStore Efficiency Report:")
    # Pass the cursor so the function extracts headers automatically.
    DBUtils.print_formatted_table(cursor, results, [15, 20, 20, 25])
    cursor.close()

def client_query_popular_products(conn):
    cursor = conn.cursor()
    query = """
        SELECT product_name, COUNT(*) AS total_orders
        FROM orders o
        NATURAL JOIN products_in_order
        NATURAL JOIN products
        GROUP BY product_id
        ORDER BY total_orders DESC
        LIMIT 15;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\nTop 15 Popular Products:")
    DBUtils.print_formatted_table(cursor, results, [25, 15])
    cursor.close()

def client_query_popular_aisles(conn):
    cursor = conn.cursor()
    query = """
        SELECT aisle, COUNT(*) AS order_count
        FROM orders o
        NATURAL JOIN products_in_order
        NATURAL JOIN products
        NATURAL JOIN aisles
        GROUP BY aisle
        ORDER BY order_count DESC
        LIMIT 15;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\nTop 15 Popular Aisles:")
    DBUtils.print_formatted_table(cursor, results, [30, 15])
    cursor.close()

# ----- UI Helper -----
def show_client_options():
    print("\nClient Options:")
    print("1 - View store efficiency")
    print("2 - Query popular products")
    print("3 - Query popular aisles")
    print("q - Quit")
    return input("Enter an option: ").lower().strip()

def quit_ui():
    print("Goodbye! Good luck with your future data analysis!")
    sys.exit(0)

# ----- Main Application Flow for Client -----
def main():
    # Connect using the read-only account
    conn = DBUtils.get_conn("appclient", "client")
    if not conn:
        print("Failed to connect to the database.")
        sys.exit(1)

    print("Welcome to the Supermarket Client Application")
    print("Press enter (with no text) to exit")
    
    # Prompt for login; if either username or password is empty, exit.
    while True:
        username = input("Enter your username: ").strip()
        if username == "":
            print("Username was empty. Exiting")
            sys.exit(0)
        password = input("Enter your password: ").strip()
        if password == "":
            print("Password was empty. Exiting.")
            sys.exit(0)
        is_auth, is_admin = DBUtils.authenticate_user(conn, username, password)
        if not is_auth:
            print("Username or password is incorrect. Please try again.")
            continue
        break

    print(f"Welcome, {username}!")

    # Main loop for client operations
    while True:
        option = show_client_options()
        if option == "1":
            client_view_store_efficiency(conn)
        elif option == "2":
            client_query_popular_products(conn)
        elif option == "3":
            client_query_popular_aisles(conn)
        elif option == "q":
            quit_ui()
        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    main()
