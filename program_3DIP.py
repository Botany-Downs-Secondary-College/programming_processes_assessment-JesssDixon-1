#from asyncio.windows_events import NULL
import tkinter as tk
from tkinter import ttk
from tkinter import * #should import all modules
import psycopg2
conn = psycopg2.connect(
    database="items", user="postgres", password="1234", host="127.0.0.1", port="5432"
)

cursor = conn.cursor()

cursor.execute("select * from items")
cursor.execute("insert into items values(%s, %s, %s, %s, %s)", (1, "apple", "hi", "hello", "beans"))
cursor.execute("select * from items")

print(cursor.fetchall())
conn.close()


db = psycopg2.connect(host="localhost", database="items", user="postgres", password="1234")

mycursor = db.cursor()

#action_types = ["Discuss", "Decide", "Review", "Contact", "Finish", "FYI"]
#priorities = ["Urgent High-Priority", "Urgent Low-Priority", "Non-Urgent High-Priority", "Non-Urgent Low-Priority"]

class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #Window setup
        self.title("Meeting Agenda")
        self['background'] = '#fff8f0'
        width= self.winfo_screenwidth()
        height= self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        #Navigation mechanism setup
        container = tk.Frame(self)
        container.grid(row = 0,column = 0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for page in (Meetings, MeetingX, Item, Actions, New_Item, New_Meeting):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Meetings)

    def show_frame(self, cont): #raises frame to top
        frame = self.frames[cont]
        frame.tkraise()

class Meetings(tk.Frame):
    def __init__(self, parent, controller):     
        tk.Frame.__init__(self, parent)
        self['background'] = '#fff8f0'
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", bg = "#9dd9d2").grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", command=lambda: controller.show_frame(Actions), bg = "#9dd9d2").grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting), bg = "#9dd9d2").grid(row = 0,column = 2)

        label = tk.Label(self, text="My Meetings", bg = "#fff8f0")
        label.grid(row=1, column=2, columnspan=3) # Update when I know how many columns there will be

        # Meeting list - this should become a for loop that prints meeting details for each meeting
        open_pg_meeting = tk.Button(self, text="Meeting X", command=lambda: controller.show_frame(MeetingX)).grid(row = 3,column = 3)

class MeetingX(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['background'] = '#fff8f0'

        label = tk.Label(self, text="Meeting XYZ")
        label.grid(row=1, column=3, columnspan=3)

        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meetings), bg = "#9dd9d2").grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", command=lambda: controller.show_frame(Actions), bg = "#9dd9d2").grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting), bg = "#9dd9d2").grid(row = 0,column = 2)
        navbar_new_item = tk.Button(self, text="New Item", command=lambda: controller.show_frame(New_Item), bg = "#9dd9d2").grid(row = 0,column = 3)

        label = tk.Label(self, text="Items List").grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

        #Item list - this should become a for loop that prints meeting details for each meeting
        open_pg_items = tk.Button(self, text="Item", command=lambda: controller.show_frame(Item)).grid(row = 2,column = 2)

class Actions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['background'] = '#fff8f0'
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meetings), bg = "#9dd9d2").grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", bg = "#9dd9d2").grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting), bg = "#9dd9d2").grid(row = 0,column = 2)

        label = tk.Label(self, text="Actions list").grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

class Item(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Item A")
        label.grid(row=1, column=3, columnspan=3)
        self['background'] = '#fff8f0'
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meetings), bg = "#9dd9d2").grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", command=lambda: controller.show_frame(Actions), bg = "#9dd9d2").grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting), bg = "#9dd9d2").grid(row = 0,column = 2)

        label = tk.Label(self, text="Items List").grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

class New_Item(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meetings), bg = "#9dd9d2").grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", bg = "#9dd9d2").grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting), bg = "#9dd9d2").grid(row = 0,column = 2)
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting), bg = "#9dd9d2").grid(row = 0,column = 3)

        def submit():
            controller.show_frame(MeetingX)
            print(item_name)
            item_name1 = item_name_var.get()
            priority1 = priority_var.get()
            item_des1 = item_des_var.get()
            action_type1 = action_type_var.get()
            est_time1 = est_time_var.get()
            cursor.execute("select * from items")

            cursor.execute("insert into items values(%s, %s, %s, %s, %s)", (item_name, priority, item_des, action_type, est_time))

            cursor.execute("select * from items")

            print(cursor.fetchall())
        
        # New Item Form ~~~
        heading = tk.Label(self, text="Add a New Item").grid(row=1, column=1)

        item_name = tk.Label(self, text="Item Name").grid(row=2, column=0)
        item_name_var = ttk.Entry(self).grid(row=2, column=1)

        priority = tk.Label(self, text="Priority").grid(row=3, column=0) #make this a dropdown
        priority_var = ttk.Entry(self).grid(row=3, column=1)

        item_des = tk.Label(self, text="Item Description").grid(row=4, column=0)
        item_des_var = ttk.Entry(self).grid(row=4, column=1)

        action_type = tk.Label(self, text="Action Type").grid(row=5, column=0) #make this a dropdown
        action_type_var = ttk.Entry(self).grid(row=5, column=1)

        est_time = tk.Label(self, text="Estimated Time").grid(row=6, column=0)
        est_time_var = ttk.Entry(self).grid(row=6, column=1)
    
        add = tk.Button(self, text="Add Item to Agenda", bg="#ff8811", command=submit).grid(row=8, column=1)

class New_Meeting(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meetings)).grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions").grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting)).grid(row = 0,column = 2)

        label = tk.Label(self, text="Actions list").grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

if __name__ == "__main__":
    testObj = main()
    testObj.mainloop()