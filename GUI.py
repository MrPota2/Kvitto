import kvitto
import os
import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

H1 = ("Helvetica", 14, "bold")
H2 = ("Helvetica", 10, "bold")
H3 = ("Helvetica", 8, "bold")


window = Tk()
window.title("Kvitto - Main Menu")

# functions
def get_trips():
    trip_list = []
    for file in os.listdir("db"):
        if file.endswith(".db"):
            trip_list.append(file[:-3])
    trip.set(tuple(trip_list))


### toplevels
def add_trip():
    def create_trip():
        kvitto.create_db(trip_name.get())
        new_trip.destroy()
        get_trips()


    new_trip = Toplevel(window)
    new_trip.title("Add trip")

    lbl_trip = Label(new_trip, text="Trip name")
    lbl_trip.grid(row=0, column=0, padx=5, pady=5, sticky=W)

    trip_name = StringVar()
    ent_trip = Entry(new_trip, width=20, textvariable=trip_name)
    ent_trip.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    btn_confirm = Button(new_trip, text="Confirm", width=20, command=create_trip)
    btn_confirm.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=W)

def trip_menu(event):
    def get_receipts():
        conn = kvitto.create_connection(trip_name)
        receipts = []
        receipt_table = conn.execute("SELECT * FROM receipt;")
        sum_per_receipt = conn.execute("SELECT timestamp, SUM(price*qty) AS sum FROM item GROUP BY timestamp;")
        for receipt in receipt_table:
            sum_found = False
            for sum in sum_per_receipt:
                if receipt[0] == sum[0]:
                    receipts.append(receipt + (sum[1],))
                    sum_found = True
                    break
            if not sum_found:
                receipts.append(receipt + (0,))
        for receipt in receipts:
            trw_receipts.insert("", "end", values=receipt)
        #sum of all receipts
        total = conn.execute("SELECT SUM(price*qty) AS sum FROM item;")
        total = total.fetchone()[0]
        total = round(total, 2)
        receipts_sum.set(total)
        conn.close()
        print('disconnected from db')

    def get_users():
        trw_users.delete(*trw_users.get_children())
        conn = kvitto.create_connection(trip_name)
        user_table = conn.execute("SELECT name FROM user;")
        for user in user_table:
            trw_users.insert("", "end", values=user)
        conn.close()
        print('disconnected from db')

    def receipt_menu(event):
        receipt_timestamp = trw_receipts.item(trw_receipts.selection())['values'][0]
        receipt_store = trw_receipts.item(trw_receipts.selection())['values'][1]
        receipt_title = receipt_timestamp + " " + receipt_store

        def get_items():
            conn = kvitto.create_connection(trip_name)
            item_table = conn.execute("SELECT item.name AS Item, item.price AS Price, item.qty AS Quantity, item.price*item.qty AS Total,  item.payor AS Payor FROM item WHERE timestamp=?;", (receipt_timestamp,))
            for item in item_table:
                trw_items.insert("", "end", values=item)
            conn.close()
            print('disconnected from db')

        win_receipt = Toplevel(win_trip)
        win_receipt.title(receipt_title)

        lbl_items = Label(win_receipt, text="Items", font=(H1))
        lbl_items.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        scroll_items = Scrollbar(win_receipt, orient=VERTICAL)
        scroll_items.grid(row=1, column=3, padx=(0, 5), pady=5, sticky=NS)
        trw_items = ttk.Treeview(win_receipt, columns=(1, 2, 3, 4, 5), show='headings', height=10)
        trw_items.grid(row=1, column=0, columnspan=3, padx=(5, 0), pady=5, sticky=W)
        trw_items.heading(1, text="Item")
        trw_items.heading(2, text="Price")
        trw_items.heading(3, text="Qty")
        trw_items.heading(4, text="Total")
        trw_items.heading(5, text="Payor")
        trw_items.column(1, width=140)
        trw_items.column(2, width=100)
        trw_items.column(3, width=100)
        trw_items.column(4, width=80)
        trw_items.column(5, width=180)
        scroll_items.config(command=trw_items.yview)

        get_items()



    def new_receipt():
        def on_entry_click(event):
            """function that gets called whenever entry is clicked"""
            if ent_timestamp.get() == '31-12-2023 12:59:59':
                ent_timestamp.delete(0, "end") # delete all the text in the ent_timestamp
                ent_timestamp.insert(0, '') #Insert blank for user input
                ent_timestamp.config(fg = 'black')
        def on_focusout(event):
            if ent_timestamp.get() == '':
                ent_timestamp.insert(0, '31-12-2023 12:59:59')
                ent_timestamp.config(fg = 'grey')

        def create_receipt():
            conn = kvitto.create_connection(trip_name)
            victim = kvitto.username_to_id(conn, receipt_victim.get())
            kvitto.new_receipt(conn, txt_receipt.get('1.0', 'end-1c'), receipt_store.get(), victim)
            #text = txt_receipt.get('1.0', 'end-1c')
            #time = kvitto.get_timestamp(text)
            #conn = kvitto.create_connection(trip_name)
            #conn.execute("INSERT INTO receipt (timestamp, #store, victim) VALUES (?, ?, ?);", (time, #receipt_store.get(), receipt_victim.get()))
            #conn.commit()
            #conn.close()
            #print('disconnected from db')
            #kvitto.get_items(text)
            #items=new_receipt.destroy()
            #for item in items:
            #    kvitto.create_item(trip_name, item)
            get_receipts()

        new_receipt = Toplevel(win_trip)
        new_receipt.title("Add receipt")

        lbl_timestamp = Label(new_receipt, text="Timestamp:")
        lbl_timestamp.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        receipt_timestamp = StringVar()
        ent_timestamp = Entry(new_receipt, width=20, textvariable=receipt_timestamp)
        ent_timestamp.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        
        ent_timestamp.insert(0, '31-12-2023 12:59:59')
        ent_timestamp.config(fg = 'grey')
        ent_timestamp.bind('<FocusIn>', on_entry_click)
        ent_timestamp.bind('<FocusOut>', on_focusout)

        lbl_store = Label(new_receipt, text="Store:")
        lbl_store.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        receipt_store = StringVar()
        ent_store = Entry(new_receipt, width=20, textvariable=receipt_store)
        ent_store.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        lbl_victim = Label(new_receipt, text="Victim:")
        lbl_victim.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        receipt_victim = StringVar()
        ent_victim = Entry(new_receipt, width=20, textvariable=receipt_victim)
        ent_victim.grid(row=2, column=1, padx=5, pady=5, sticky=W)

        lbl_receipt = Label(new_receipt, text="Receipt text:", font=(H1))
        lbl_receipt.grid(row=3, column=0, padx=5, pady=5, sticky=W)


        txt_receipt = Text(new_receipt, width=40, height=50)
        txt_receipt.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=W)

        btn_confirm = Button(new_receipt, text="Confirm", width=20, command=create_receipt)
        btn_confirm.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky=S)

    def new_user():
        def create_user():
            conn = kvitto.create_connection(trip_name)
            conn.execute("INSERT INTO user (name) VALUES (?);", (user_name.get(),))
            conn.commit()
            conn.close()
            print('disconnected from db')
            new_user.destroy()
            get_users()
    
        new_user = Toplevel(win_trip)
        new_user.title("Add user")

        lbl_user = Label(new_user, text="Username:")
        lbl_user.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        user_name = StringVar()
        ent_user = Entry(new_user, width=20, textvariable=user_name)
        ent_user.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        btn_confirm = Button(new_user, text="Confirm", width=20, command=create_user)
        btn_confirm.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=W)


    trip_name = lst_trip.get(lst_trip.curselection())

    win_trip = Toplevel(window)
    win_trip.title(trip_name)

    # receipts
    lbl_receipts = Label(win_trip, text="Receipts", font=(H1))
    lbl_receipts.grid(row=0, column=0, padx=5, pady=5, sticky=W)

    scroll_receipts = Scrollbar(win_trip, orient=VERTICAL)
    scroll_receipts.grid(row=1, column=3, padx=(0,5), pady=5, sticky=NS)
    trw_receipts = ttk.Treeview(win_trip, columns=(1,2,3,4), show='headings', height=10)
    trw_receipts.grid(row=1, column=0, columnspan=3, padx=(5, 0), pady=5, sticky=W)
    trw_receipts.heading(1, text="Date")
    trw_receipts.heading(2, text="Store")
    trw_receipts.heading(3, text="Victim")
    trw_receipts.heading(4, text="Total")
    trw_receipts.column(1, width=140)
    trw_receipts.column(2, width=100)
    trw_receipts.column(3, width=100)
    trw_receipts.column(4, width=80)
    trw_receipts.bind("<Double-1>", receipt_menu)
    scroll_receipts['command'] = trw_receipts.yview

    btn_new_receipt = Button(win_trip, text="New receipt", width=20, command=new_receipt)
    btn_new_receipt.grid(row=2, column=0, padx=5, pady=5, sticky=N)

    lbl_receipts_sum = Label(win_trip, text="Total:", font=(H2))
    lbl_receipts_sum.grid(row=2, column=1, padx=(5,0), pady=5, sticky=E)

    receipts_sum = StringVar()
    ent_receipts_sum = Entry(win_trip, width=8, textvariable=receipts_sum, state='readonly')
    ent_receipts_sum.grid(row=2, column=2, padx=(0,5), pady=5, sticky=W)
    get_receipts()

    # Users
    lbl_users = Label(win_trip, text="Users", font=(H1))
    lbl_users.grid(row=0, column=4, padx=(5,0), pady=5, sticky=W)

    scroll_users = Scrollbar(win_trip, orient=VERTICAL)
    scroll_users.grid(row=1, column=7, padx=(0,5), pady=5, sticky=NS)
    trw_users = ttk.Treeview(win_trip, columns=(1,2,3), show='headings', height=10)
    trw_users.grid(row=1, column=4, columnspan=3, padx=(5, 0), pady=5, sticky=W)
    trw_users.heading(1, text="Name")
    trw_users.heading(2, text="Unpaid")
    trw_users.heading(3, text="Total")
    trw_users.column(1, width=140)
    trw_users.column(2, width=80)
    trw_users.column(3, width=80)
    scroll_users['command'] = trw_users.yview
    get_users()

    btn_new_user = Button(win_trip, text="New user", width=20, command=new_user)
    btn_new_user.grid(row=2, column=4, columnspan=3, padx=5, pady=5)



# elements
lbl_trip = Label(window, text="Trips")
lbl_trip.grid(row=0, column=0, padx=5, pady=5, sticky=W)

scroll_trip = Scrollbar(window, orient=VERTICAL)
scroll_trip.grid(row=1, column=1, padx=(0,5), pady=5, sticky=NS)
trip = StringVar()
lst_trip = Listbox(window, width=20, height=10, selectmode=SINGLE, listvariable=trip)
lst_trip.grid(row=1, column=0, padx=(5,0), pady=5, sticky=W)
scroll_trip['command'] = lst_trip.yview
get_trips()
lst_trip.bind("<Double-1>", trip_menu)

btn_add_trip = Button(window, text="Add trip", width=20, command=add_trip)
btn_add_trip.grid(row=2, column=0, padx=5, pady=5, sticky=N)




window.mainloop()