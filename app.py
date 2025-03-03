"""
Student Name(s): Jonathan Lin, Enoch Luk
Student Email(s): jonathan@caltech.edu, eluk@caltech.edu

High-Level Program Overview:
This is a command-line interface skeleton for a supermarket
database application. It provides functionalities for both client and
admin users. Clients perform read-only queries while admins can add or
update data.
"""

import sys
import mysql.connector
import mysql.connector.errorcode as errorcode
from typing import Any, Optional

# ----------------------------------------------------------------------
# Database Connection
# ----------------------------------------------------------------------
def get_conn(user: str, password: str) -> Optional[mysql.connector.connection.MySQLConnection]:
    """
    Establishes and returns a MySQL database connection.

    Args:
        user (str): MySQL username.
        password (str): MySQL password.

    Returns:
        MySQLConnection object or None if the connection fails.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database="final2"

        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# ----------------------------------------------------------------------
# Client Functions
# ----------------------------------------------------------------------
def client_query_popular_products(conn: mysql.connector.connection.MySQLConnection) -> None:
    """
    Queries and displays popular products based on order volume.
    """
    cursor = conn.cursor()
    query = """
        SELECT product_name, COUNT(*) AS total_orders
        FROM orders
        JOIN order_products USING (order_id)
        JOIN products USING (product_id)
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

def client_query_popular_aisles(conn: mysql.connector.connection.MySQLConnection) -> None:
    """
    Queries and displays the most popular aisles based on order volume.
    """
    cursor = conn.cursor()
    query = """
        SELECT aisle, COUNT(*) AS order_count
        FROM orders
        JOIN order_products USING (order_id)
        JOIN products USING (product_id)
        JOIN aisles USING (aisle_id)
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

def client_view_customer_order_history(conn: mysql.connector.connection.MySQLConnection, customer_id: int) -> None:
    """
    Queries and displays the order history for a specific customer.
    """
    cursor = conn.cursor()
    query = """
        SELECT order_id, product_name, add_to_cart_order
        FROM orders
        JOIN order_products USING (order_id)
        JOIN products USING (product_id)
        WHERE user_id = %s;
    """
    cursor.execute(query, (customer_id,))
    results = cursor.fetchall()

    if not results:
        print("\nNo order history found for this customer.")
    else:
        print("\nOrder History:")
        for order_id, product, cart_position in results:
            print(f"Order {order_id}: {product} (Added at position {cart_position})")

    cursor.close()

# ----------------------------------------------------------------------
# Admin Functions
# ----------------------------------------------------------------------
def admin_add_new_order(conn: mysql.connector.connection.MySQLConnection) -> None:
    """
    Adds a new order to the database.
    """
    cursor = conn.cursor()
    user_id = input("\nEnter Customer ID: ")
    
    query = "INSERT INTO orders (user_id, order_dow, order_hour_of_day) VALUES (%s, DAYOFWEEK(NOW()), HOUR(NOW()))"
    cursor.execute(query, (user_id,))
    conn.commit()
    
    print(f"New order created with Order ID: {cursor.lastrowid}")
    cursor.close()

def admin_update_product(conn: mysql.connector.connection.MySQLConnection) -> None:
    """
    Updates product details, such as name, aisle, or department.
    """
    cursor = conn.cursor()
    product_id = input("\nEnter Product ID to update: ")
    new_name = input("Enter new product name: ")

    query = "UPDATE products SET product_name = %s WHERE product_id = %s"
    cursor.execute(query, (new_name, product_id))
    conn.commit()

    print("Product updated successfully.")
    cursor.close()

# ----------------------------------------------------------------------
# Login Functions
# ----------------------------------------------------------------------
def login_user(user_role: str) -> Optional[mysql.connector.connection.MySQLConnection]:
    """
    Handles user login for admin or client.

    Args:
        user_role (str): Either 'admin' or 'client'.

    Returns:
        MySQLConnection object or None if authentication fails.
    """
    username = "appadmin" if user_role == "admin" else "appclient"
    password = input(f"Enter {user_role} password: ")
    
    conn = get_conn(username, password)
    if conn:
        print(f"\nWelcome {user_role}! Successfully logged in.")
        return conn
    else:
        print("Login failed. Check your credentials.")
        return None

# ----------------------------------------------------------------------
# UI Functions
# ----------------------------------------------------------------------
def show_client_options() -> str:
    """
    Displays client options and returns the selected option.
    """
    print("\nClient Options:")
    print("1 - Query popular products")
    print("2 - Query popular aisles")
    print("3 - View customer order history")
    print("q - Quit")
    return input("Enter an option: ").lower().strip()

def show_admin_options() -> str:
    """
    Displays admin options and returns the selected option.
    """
    print("\nAdmin Options:")
    print("1 - Add a new order")
    print("2 - Update product details")
    print("q - Quit")
    return input("Enter an option: ").lower().strip()

def quit_ui() -> None:
    """
    Exits the program after displaying a goodbye message.
    """
    print("Goodbye!")
    sys.exit(0)

# ----------------------------------------------------------------------
# Main Program
# ----------------------------------------------------------------------
def main() -> None:
    """
    Initializes the database connection and starts the application.
    """
    print("Welcome to the Supermarket Database System")
    user_type = input("Are you logging in as (admin/client)? ").strip().lower()

    if user_type not in ["admin", "client"]:
        print("Invalid user type. Exiting.")
        quit_ui()

    conn = login_user(user_type)
    if not conn:
        quit_ui()

    while True:
        if user_type == "client":
            option = show_client_options()
            if option == "1":
                client_query_popular_products(conn)
            elif option == "2":
                client_query_popular_aisles(conn)
            elif option == "3":
                customer_id = int(input("Enter customer ID: "))
                client_view_customer_order_history(conn, customer_id)
            elif option == "q":
                quit_ui()
            else:
                print("Invalid option. Try again.")

        elif user_type == "admin":
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
