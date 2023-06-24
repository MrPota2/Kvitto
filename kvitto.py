import sqlite3
from sqlite3 import Error
import re


def create_connection(trip_name):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(r'db/' + trip_name + '.db')
        print("Connected to database")
        return conn
    except Error as e:
        print(e)


def create_db(trip_name):
    database = r"db/" + trip_name + ".db"

    ### SQL statements ###
    # Create user table
    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                                        qty INTEGER NOT NULL,
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
    conn = create_connection(trip_name)
    if conn is not None:
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_receipt_table)
        create_table(conn, sql_create_item_table)
        create_table(conn, sql_create_status_table)
        conn.commit()
        conn.close()
        print("Database created!")
    else:
        print("Error! cannot create the database connection.")

    


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
    """
    sql = ''' INSERT INTO receipt(timestamp,store,victim)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (timestamp,store,victim))
    conn.commit()

def create_item(conn, timestamp, name, price, qty):
    """
    Create a new item into the item table
    :param conn:
    :param item:
    """
    sql = ''' INSERT INTO item(timestamp,name,price,qty)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (timestamp,name,price,qty))
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


# Get receipt data
def get_timestamp(text):
    """
    Get receipt data
    :param text:
    :return: receipt data
    """
    # Get timestamp
    timestamp = re.search(r'\d{2}.\d{2}.\d{2} \d{2}:\d{2}', text).group()
    print('before: ', timestamp)
    d = timestamp[0:2]
    m = timestamp[3:5]
    y = timestamp[6:8]
    timestamp = '20' + y + '-' + m + '-' + d + ' ' + timestamp[9:14]
    print('after: ', timestamp)
    return timestamp

def get_items(text):
    """
    Get receipt data
    :param text:
    :return: receipt data
    """
    all_products = re.search(r'start([\s\S]*?)end', text).group()
    all_products = all_products.split('\n')
    #remove first and last element
    all_products.pop(0)
    all_products.pop()
    # connect item to price
    items = []
    for product in all_products:
        product = product.replace('0%','15%').replace('25%','15%').split(' 15% ')
        items.append([product[0], float(product[-1].replace(',','.'))])
        items[-1].append(1)
    # merge duplicate items
    for i in range(len(items)):
        for j in range(i+1,len(items)):
            if items[i][0] == items[j][0]:
                items[i][2] += items[j][2]
                items[j][2] = 0
    # remove duplicates
    items = [item for item in items if item[2] != 0]
    print(items)
    return items

def new_receipt(conn, receipt, store, victim):
    """
    Get receipt data
    :param conn:
    :param receipt:
    :param store:
    :param victim:
    :return: receipt data
    """
    timestamp = get_timestamp(receipt)
    create_receipt(conn, timestamp, store, victim)
    for items in get_items(receipt):
        create_item(conn, timestamp, items[0], items[1], items[2])


def main():
    conn = create_db('hvasser')
    #conn = create_connection('hvasser')
    create_user(conn, ('Johan',))
    create_user(conn, ('Erik',))
    create_user(conn, ('Kalle',))
    store = 'SPAR'
    victim = 'Johan'
    receipt = open('test.txt', 'r').read()
    new_receipt(conn, receipt, store, victim)
    

    

#main()