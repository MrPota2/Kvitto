import sqlite3
from sqlite3 import Error

# Create database
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


# Insert into database
def create_user(conn, user):
    """
    Create a new user into the user table
    :param conn:
    :param user:
    :return: user id
    """
    sql = ''' INSERT INTO user(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def create_receipt(conn, timestamp, store, victim):
    """
    Create a new receipt into the receipt table
    :param conn:
    :param receipt:
    :return: receipt id
    """
    sql = ''' INSERT INTO receipt(timestamp,store,victim)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (timestamp,store,victim))
    conn.commit()
    return cur.lastrowid

def create_item(conn, timestamp, name, price, payor):
    """
    Create a new item into the item table
    :param conn:
    :param item:
    """
    sql = ''' INSERT INTO item(timestamp,name,price)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (timestamp,name,price))
    conn.commit()

def create_status(conn, timestamp, user, status):
    """
    Create a new status into the status table
    :param conn:
    :param status:
    """
    sql = ''' INSERT INTO status(timestamp,user,status)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (timestamp,user,status))
    conn.commit()



def create_db():
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
                                        payor text,
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

def main():
    create_db()
