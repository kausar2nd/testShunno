import mysql.connector


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="shunnowaste_db",
    )
    return connection
