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
        receipt_table = conn.execute("SELECT * FROM receipt")
        sum_per_receipt = conn.execute("SELECT timestamp, SUM(price*qty) AS sum FROM item GROUP BY timestamp")
        for receipt in receipt_table:
            for sum in sum_per_receipt:
                if receipt[0] == sum[0]:
                    receipts.append(receipt + (sum[1],))
        for receipt in receipts:
            trw_receipts.insert("", "end", values=receipt)
        #sum of all receipts
        total = conn.execute("SELECT SUM(price*qty) AS sum FROM item")
        total = total.fetchone()[0]
        total = round(total, 2)
        receipts_sum.set(total)
        conn.close()
        print('disconnected from db')

    def get_users():
        conn = kvitto.create_connection(trip_name)
        user_table = conn.execute("SELECT name FROM user")
        for user in user_table:
            trw_users.insert("", "end", values=user)
        conn.close()
        print('disconnected from db')

    def receipt_menu():
        None

    def new_receipt():
        None

    def new_user():
        None

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