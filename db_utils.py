# db_utils.py
import mysql.connector
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
    def value_exists(conn, table_name, column_name, value):
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

