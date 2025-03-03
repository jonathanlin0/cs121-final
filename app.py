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

def get_conn() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes and returns a MySQL database connection.

    Returns:
        A MySQLConnection object.
    """
    # Implementation for database connection.
    pass

# ----------------------------------------------------------------------
# Client Functions
# ----------------------------------------------------------------------
def client_query_popular_products(
        conn: mysql.connector.connection.MySQLConnection) -> None:
    """
    Queries and displays popular products based on order volume.

    Args:
        conn: A MySQLConnection object.

    Returns:
        None.
    """
    # Implementation to fetch and display top popular products.
    pass

def client_query_popular_aisles(
        conn: mysql.connector.connection.MySQLConnection) -> None:
    """
    Queries and displays the most popular aisles based on order volume.

    Args:
        conn: A MySQLConnection object.

    Returns:
        None.
    """
    # Implementation to fetch and display popular aisles.
    pass

def client_view_customer_order_history(
        conn: mysql.connector.connection.MySQLConnection,
        customer_id: int) -> None:
    """
    Queries and displays the order history for a specific customer.

    Args:
        conn: A MySQLConnection object.
        customer_id: The ID of the customer whose order history is to be
                     displayed.

    Returns:
        None.
    """
    # Implementation to fetch and display order history for the customer.
    pass

# ----------------------------------------------------------------------
# Admin Functions
# ----------------------------------------------------------------------
def admin_add_new_order(
        conn: mysql.connector.connection.MySQLConnection) -> None:
    """
    Adds a new order to the database.

    Args:
        conn: A MySQLConnection object.

    Returns:
        None.
    """
    # Implementation to add a new order.
    pass

def admin_update_product(
        conn: mysql.connector.connection.MySQLConnection) -> None:
    """
    Updates product details, such as name, aisle, or department.

    Args:
        conn: A MySQLConnection object.

    Returns:
        None.
    """
    # Implementation to update product information.
    pass

# ----------------------------------------------------------------------
# Login Functions
# ----------------------------------------------------------------------
def login_admin() -> None:
    """
    Logs in an admin.

    Returns:
        None.
    """
    # Implementation for admin login.
    pass

def login_client() -> None:
    """
    Logs in a client.

    Returns:
        None.
    """
    # Implementation for client login.
    pass

# ----------------------------------------------------------------------
# UI Functions
# ----------------------------------------------------------------------
def show_client_options() -> str:
    """
    Displays client options and returns the selected option.

    Returns:
        The user's selected option as a string.
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

    Returns:
        The user's selected option as a string.
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
    print("Good bye!")
    sys.exit(0)

def main() -> None:
    """
    Initializes the database connection and displays a startup message.

    Returns:
        None.
    """
    # Establish a database connection.
    conn = get_conn()

    # Placeholder for future logic to prompt user actions.
    print("Application initialized. "
          "Add your program logic here.")

if __name__ == '__main__':
    main()
