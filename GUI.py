import kvitto
import os
import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox




window = Tk()
window.title("Kvitto - Main Menu")

# functions
def get_trips():
    trip_list = []
    for file in os.listdir("db"):
        if file.endswith(".db"):
            trip_list.append(file[:-3])
    trip.set(tuple(trip_list))


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


# elements
lbl_trip = Label(window, text="Trips")
lbl_trip.grid(row=0, column=0, padx=5, pady=5, sticky=W)

trip = StringVar()
lst_trip = Listbox(window, width=20, height=10, selectmode=SINGLE, listvariable=trip)
lst_trip.grid(row=1, column=0, padx=5, pady=5, sticky=W)
get_trips()


btn_add_trip = Button(window, text="Add trip", width=20, command=add_trip)
btn_add_trip.grid(row=2, column=0, padx=5, pady=5, sticky=N)


window.mainloop()