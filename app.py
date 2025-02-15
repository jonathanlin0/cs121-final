"""
Supermarket Stock Optimization Application
Student names: Jonathan Lin, Enoch Luk
Student emails: jonathan@caltech.edu, eluk@caltech.edu

This is the command-line application interface for the Supermarket Stock
Optimization project. It supports two types of users:
  - Client users (store managers/analysts) can query insights such as popular
    products, sales trends, and aisle performance.
  - Admin users (regional managers) have additional options to update
    inventory, add or remove products, etc.

Each function below is a placeholder for the corresponding functionality.
"""

import sys
import mysql.connector
import mysql.connector.errorcode as errorcode
from typing import NoReturn, Optional, List
import datetime  # For date manipulation in future implementations

DEBUG: bool = True

def get_conn() -> mysql.connector.MySQLConnection:
    """
    Establish and return a connection to the MySQL database.
    
    Returns:
        mysql.connector.MySQLConnection: A connection object if successful.
    
    Raises:
        Exits the program if the connection fails.
    """
    # TODO: Implement actual connection logic using
    # mysql.connector.connect(...)
    pass

def query_popular_products(
    conn: mysql.connector.MySQLConnection, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
) -> None:
    """
    Query to identify the most popular products in a given date range.
    
    Parameters:
        conn (mysql.connector.MySQLConnection): A connection object to the
            database.
        start_date (Optional[str]): Start date in 'YYYY-MM-DD' format.
            Defaults to one month ago if None.
        end_date (Optional[str]): End date in 'YYYY-MM-DD' format.
            Defaults to today if None.
    
    Returns:
        None. Prints or returns the top products based on order counts.
    """
    # TODO: If start_date or end_date is None, compute defaults for the past
    # month. Then, implement query execution and processing of results.
    pass

def query_sales_trends(
    conn: mysql.connector.MySQLConnection, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
) -> List[str]:
    """
    Query to retrieve a list of trending products in a given date range.
    
    Parameters:
        conn (mysql.connector.MySQLConnection): A connection object to the
            database.
        start_date (Optional[str]): Start date in 'YYYY-MM-DD' format.
            Defaults to one month ago if None.
        end_date (Optional[str]): End date in 'YYYY-MM-DD' format.
            Defaults to today if None.
    
    Returns:
        List[str]: A list of product names that are trending within the
            specified date range.
    """
    # TODO: Compute default dates if start_date or end_date is None.
    # Implement query logic to determine trending products.
    # Return a list of trending product names.
    return []

def query_popular_aisles(
    conn: mysql.connector.MySQLConnection, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
) -> None:
    """
    Query to find the most popular aisles based on order volume in a date range.
    
    Parameters:
        conn (mysql.connector.MySQLConnection): A connection object to the
            database.
        start_date (Optional[str]): Start date in 'YYYY-MM-DD' format.
            Defaults to one month ago if None.
        end_date (Optional[str]): End date in 'YYYY-MM-DD' format.
            Defaults to today if None.
    
    Returns:
        None. Prints or returns the most frequented aisles.
    """
    # TODO: Compute default date values if None and implement query execution.
    pass

def update_stock_levels(
    conn: mysql.connector.MySQLConnection
) -> None:
    """
    Admin functionality to update stock levels for products.
    
    Parameters:
        conn (mysql.connector.MySQLConnection): A connection object to the
            database.
    
    Returns:
        None.
    """
    # TODO: Implement functionality to update stock levels in the database.
    pass

def add_new_product(
    conn: mysql.connector.MySQLConnection
) -> None:
    """
    Admin functionality to add a new product to the inventory.
    
    Parameters:
        conn (mysql.connector.MySQLConnection): A connection object to the
            database.
    
    Returns:
        None.
    """
    # TODO: Implement functionality to insert a new product into the database.
    pass

def delete_product(
    conn: mysql.connector.MySQLConnection
) -> None:
    """
    Admin functionality to delete a product from the inventory.
    
    Parameters:
        conn (mysql.connector.MySQLConnection): A connection object to the
            database.
    
    Returns:
        None.
    """
    # TODO: Implement functionality to remove a product from the database.
    pass

def show_client_options(
    conn: mysql.connector.MySQLConnection
) -> None:
    """
    Display command-line options for client users and process input.
    
    Parameters:
        conn (mysql.connector.MySQLConnection): A connection object to the
            database.
    
    Returns:
        None.
    """
    print("=== Client Options ===")
    print("1. View Most Popular Products in a Date Range")
    print("2. View Trending Products in a Date Range")
    print("3. View Most Popular Aisles in a Date Range")
    print("q. Quit")
    
    # TODO: Process user input, prompt for optional start and end dates,
    # then call the corresponding query functions.
    pass

def show_admin_options(
    conn: mysql.connector.MySQLConnection
) -> None:
    """
    Display command-line options for admin users and process input.
    
    Parameters:
        conn (mysql.connector.MySQLConnection): A connection object to the
            database.
    
    Returns:
        None.
    """
    print("=== Admin Options ===")
    print("1. Update Stock Levels")
    print("2. Add New Product")
    print("3. Delete Product")
    print("q. Quit")
    
    # TODO: Process user input and call the corresponding admin functions.
    pass

def login_admin() -> None:
    """
    Logs in for an admin.

    Returns:
        None.
    """
    # TODO: Logic for logging in an admin
    pass

def login_client() -> None:
    """
    Logs in for a client.

    Returns:
        None.
    """
    # TODO: Logic for logging in a client
    pass

def main() -> None:
    """
    Main function to initialize the application.
    
    Establishes the database connection, prompts the user to select their
    role, and directs them to the appropriate menu.
    
    Returns:
        None.
    """
    # Establish database connection
    conn = get_conn()
    
    # Prompt user to select their role
    role: str = input("Enter role (admin/client): ").strip().lower()
    
    if role == "admin":
        login_admin()
        show_admin_options(conn)
    else:
        login_client()
        show_client_options(conn)
    
    # TODO: Add any additional cleanup or termination code if needed.
    pass

if __name__ == '__main__':
    main()
