import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",           
        user="root",
        password="Pari@2005",
        database="online_shopping"
    )
    return conn

