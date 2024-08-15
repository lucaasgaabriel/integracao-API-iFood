import mysql.connector

def connect_sql():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "admin",
        "database": "consumo_ifood"
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    return connection, cursor