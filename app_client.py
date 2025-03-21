# app_client.py
import sys
from db_utils import DBUtils

# ----- Client Functions (read-only queries) -----
def client_query_popular_products(conn):
    cursor = conn.cursor()
    query = """
        SELECT product_name, COUNT(*) AS total_orders
        FROM orders o
        NATURAL JOIN products_in_order
        NATURAL JOIN products
        GROUP BY product_id, product_name
        ORDER BY total_orders DESC
        LIMIT 10;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\nTop 10 Popular Products:")
    for product, count in results:
        print(f"{product}: {count} orders")
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
        LIMIT 10;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\nTop 10 Popular Aisles:")
    for aisle, count in results:
        print(f"{aisle}: {count} orders")
    cursor.close()

def client_view_customer_order_history(conn):
    try:
        customer_id = int(input("Enter customer ID: "))
    except ValueError:
        print("Invalid customer ID.")
        return

    cursor = conn.cursor()
    query = """
        SELECT order_id, order_timestamp, product_name
        FROM orders
        NATURAL JOIN products_in_order
        NATURAL JOIN products
        WHERE user_id = %s;
    """
    cursor.execute(query, (customer_id,))
    results = cursor.fetchall()

    if not results:
        print("\nNo order history found for this customer.")
    else:
        print("\nOrder History:")
        for order_id, order_timestamp, product in results:
            print(f"Order {order_id} (at {order_timestamp}): {product}")
    cursor.close()

# ----- UI Helper -----
def show_client_options():
    print("\nClient Options:")
    print("1 - Query popular products")
    print("2 - Query popular aisles")
    print("3 - View customer order history")
    print("q - Quit")
    return input("Enter an option: ").lower().strip()

def quit_ui():
    print("Goodbye!")
    sys.exit(0)

# ----- Main Application Flow for Client -----
def main():
    # Connect using the read-only account
    conn = DBUtils.get_conn("appclient", "client")
    if not conn:
        print("Failed to connect to the database.")
        sys.exit(1)

    print("Welcome to the Supermarket Client Application")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    is_auth, is_admin = DBUtils.authenticate_user(conn, username, password)
    if not is_auth:
        print("Authentication failed. Please check your credentials.")
        sys.exit(1)
    if is_admin:
        print("This application is for client users only.")
        sys.exit(1)
    print(f"Welcome, {username}!")

    # Main loop for client operations
    while True:
        option = show_client_options()
        if option == "1":
            client_query_popular_products(conn)
        elif option == "2":
            client_query_popular_aisles(conn)
        elif option == "3":
            client_view_customer_order_history(conn)
        elif option == "q":
            quit_ui()
        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    main()
