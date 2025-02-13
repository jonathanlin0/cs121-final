#!/usr/bin/env python3
"""
app.py: Command-line client application for the supermarket data analysis project.

This file contains function stubs and a basic menu-driven interface to interact with
our SQL database. Actual database functionality will be implemented later.
"""

from typing import Optional, Any

def get_conn() -> Optional[Any]:
    """
    Establishes and returns a connection to the SQL database.
    
    Returns:
        A connection object if successful, or None if the connection fails.
    """
    # TODO: Implement database connection using proper credentials and error handling.
    return None

def show_options() -> None:
    """
    Display the list of available options for the client user.
    """
    options = [
        "1. View Most Popular Products in a Date Range",
        "2. Track Sales Trends by Day of the Week in a Date Range",
        "3. Find the Most Popular Aisles Based on Order Volume in a Date Range",
        "4. Admin Login",
        "5. Exit"
    ]
    print("\n=== Main Menu ===")
    for option in options:
        print(option)

def view_popular_products(start_date: str, end_date: str, conn: Optional[Any]) -> None:
    """
    Query the database for the most popular products between start_date and end_date.

    Parameters:
        start_date (str): The starting date for the query in 'YYYY-MM-DD' format.
        end_date (str): The ending date for the query in 'YYYY-MM-DD' format.
        conn (Optional[Any]): A connection object to the database.
    
    Expected behavior:
        - Use the connection to execute the SQL query for popular products.
        - Format and display the query results.
    """
    # TODO: Implement SQL query execution and result display
    pass

def track_sales_trends(start_date: str, end_date: str, conn: Optional[Any]) -> None:
    """
    Query the database to track sales trends by day of the week between start_date and end_date.

    Parameters:
        start_date (str): The starting date for the query in 'YYYY-MM-DD' format.
        end_date (str): The ending date for the query in 'YYYY-MM-DD' format.
        conn (Optional[Any]): A connection object to the database.
    
    Expected behavior:
        - Use the connection to execute the SQL query to fetch sales trends.
        - Format and display the query results.
    """
    # TODO: Implement SQL query execution and result display
    pass

def find_popular_aisles(start_date: str, end_date: str, conn: Optional[Any]) -> None:
    """
    Query the database to find the most popular aisles based on order volume between start_date and end_date.

    Parameters:
        start_date (str): The starting date for the query in 'YYYY-MM-DD' format.
        end_date (str): The ending date for the query in 'YYYY-MM-DD' format.
        conn (Optional[Any]): A connection object to the database.
    
    Expected behavior:
        - Use the connection to execute the SQL query to retrieve aisle popularity.
        - Format and display the query results.
    """
    # TODO: Implement SQL query execution and result display
    pass

def admin_login() -> None:
    """
    Admin login function to handle administrative tasks.

    Expected behavior:
        - Prompt the admin for credentials.
        - Validate the credentials against the database.
        - Grant access to admin-specific functionality upon successful login.
    """
    # TODO: Implement admin authentication and subsequent admin actions.
    pass

def main() -> None:
    """
    Main function to run the command-line interface.

    Expected flow:
        - Establish a database connection.
        - Display the main menu options.
        - Prompt user for input.
        - For options 1-3, prompt the user for a start and end date.
        - Invoke the appropriate function based on user selection.
        - Loop until the user chooses to exit.
    """
    conn: Optional[Any] = get_conn()  # Initialize the database connection once

    while True:
        show_options()
        choice: str = input("Enter your choice: ").strip()

        if choice in {"1", "2", "3"}:
            start_date: str = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date: str = input("Enter end date (YYYY-MM-DD): ").strip()

            if choice == "1":
                view_popular_products(start_date, end_date, conn)
            elif choice == "2":
                track_sales_trends(start_date, end_date, conn)
            elif choice == "3":
                find_popular_aisles(start_date, end_date, conn)
        elif choice == "4":
            admin_login()
        elif choice == "5":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
