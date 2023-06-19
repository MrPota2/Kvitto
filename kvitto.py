import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to database")
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created")
    except Error as e:
        print(e)


def main():
    database = r"kvitto.db"

    ### SQL statements ###
    # Create user table
    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """
    
    # Create receipt table
    sql_create_receipt_table = """ CREATE TABLE IF NOT EXISTS receipt (
                                        timestamp text PRIMARY KEY,
                                        store text NOT NULL,
                                        victim text NOT NULL,
                                        FOREIGN KEY (victim) REFERENCES user (id)
                                    ); """
    
    sql_create_item_table = """ CREATE TABLE IF NOT EXISTS item (
                                        timestamp text,
                                        name text,
                                        price real NOT NULL,
                                        PRIMARY KEY (timestamp, name),
                                        FOREIGN KEY (timestamp) REFERENCES receipt (timestamp)
                                    ); """

    sql_create_status_table = """ CREATE TABLE IF NOT EXISTS status (
                                        timestamp text,
                                        user text,
                                        status text NOT NULL DEFAULT 'unpaid',
                                        PRIMARY KEY (timestamp, user),
                                        FOREIGN KEY (timestamp) REFERENCES receipt (timestamp),
                                        FOREIGN KEY (user) REFERENCES user (id)
                                    ); """

    
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_receipt_table)
        create_table(conn, sql_create_item_table)
        create_table(conn, sql_create_status_table)
        print("Database created!")
    else:
        print("Error! cannot create the database connection.")

main()
