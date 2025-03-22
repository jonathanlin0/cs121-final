# db_utils.py
import mysql.connector
from typing import List, Tuple, Any
from mysql.connector import Error

class DBUtils:
    @staticmethod
    def get_conn(db_user: str, db_password: str, host: str = "localhost", database: str = "final"):
        """
        Establish and return a MySQL database connection.
        """
        try:
            conn = mysql.connector.connect(
                host=host,
                user=db_user,
                password=db_password,
                database=database
            )
            return conn
        except Error as err:
            print(f"Error connecting to DB: {err}")
            return None

    @staticmethod
    def authenticate_user(conn, username: str, password: str):
        """
        Uses the stored function 'authenticate' to verify credentials.
        
        Returns:
            (is_authenticated, is_admin)
            is_authenticated: True if the user was successfully authenticated, else False.
            is_admin: True if the user is marked as admin.
        """
        cursor = conn.cursor()
        query = "SELECT authenticate(%s, %s), is_admin FROM user_info WHERE username = %s"
        cursor.execute(query, (username, password, username))
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return (False, False)
        auth_result, is_admin = row
        return (auth_result == 1, bool(is_admin))
    
    @staticmethod
    def value_exists(conn, table_name: str, column_name: str, value: str):
        """
        Check if a given value exists in the specified column of a table.
        
        Args:
            conn: A database connection object.
            table_name (str): The name of the table to query.
            column_name (str): The column in which to search for the value.
            value: The value to look for.
        
        Returns:
            bool: True if the value exists in the specified column, False otherwise.
        """
        cursor = conn.cursor()
        query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {column_name} = %s LIMIT 1)"
        cursor.execute(query, (value,))
        exists = cursor.fetchone()[0]
        cursor.close()
        return bool(exists)
    
    @staticmethod
    def print_formatted_table(cursor, rows : List[Tuple[Any, ...]], col_widths: List[int], headers=None):
        """
        Format and print a table of results using the specified column widths.

        Args:
            cursor: The cursor object after executing the query.
            rows (list of tuples): The rows returned from a SQL query.
            col_widths (list of int): A list of integers specifying the width of each column.
            headers (list of str, optional): The column headers to print. If not provided,
                headers are extracted from the cursor's description.

        If headers are not provided, extracts column names from the cursor's description.
        If a value's string representation is longer than the allowed width, it is truncated.
        Two spaces are added between columns for padding.
        If no rows are provided, prints a message indicating no results.
        """
        if headers is None:
            headers = [col[0] for col in cursor.description]
        
        if not rows:
            print("No results found for the requested task.")
            return

        # Print the header row with two spaces between each column.
        header_line = ""
        for idx, header in enumerate(headers):
            width = col_widths[idx] if idx < len(col_widths) else 10
            truncated_header = str(header)[:width]
            header_line += truncated_header.ljust(width) + "  "
        print(header_line)
        print("-" * len(header_line))

        # Print each row, truncating values if they exceed the allowed width.
        for row in rows:
            formatted_line = ""
            for idx, col in enumerate(row):
                width = col_widths[idx] if idx < len(col_widths) else 10
                col_str = str(col)
                if len(col_str) > width:
                    col_str = col_str[:width]
                formatted_line += col_str.ljust(width) + "  "
            print(formatted_line)
