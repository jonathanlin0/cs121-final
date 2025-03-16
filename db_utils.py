# db_utils.py
import mysql.connector
from mysql.connector import Error

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

def authenticate_user(conn, username: str, password: str):
    """
    Uses the stored function 'authenticate' to verify credentials.
    
    Returns:
        (is_authenticated, is_admin)
        is_authenticated: True if the user was successfully authenticated, else False.
        is_admin: True if the user is marked as admin.
    """
    cursor = conn.cursor()
    query = "SELECT authenticate(%s, %s), is_admin FROM users_info WHERE username = %s"
    cursor.execute(query, (username, password, username))
    row = cursor.fetchone()
    cursor.close()

    if row is None:
        return (False, False)
    auth_result, is_admin = row
    return (auth_result == 1, bool(is_admin))
