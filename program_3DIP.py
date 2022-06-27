import tkinter as tk
from tkinter import ttk
from tkinter import *
import psycopg2
conn = psycopg2.connect(database="agenda_info", user="postgres", password="1234", host="127.0.0.1", port="5432")

cursor = conn.cursor()

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
        #self.geometry("%dx%d" % (width, height))

        #Navigation mechanism setup
        container = tk.Frame(self)
        container.grid(row = 0,column = 0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for page in (Meeting, Item, Actions, New_Action, New_Item):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(Meeting)

    def show_frame(self, cont): #raises frame to top
        frame = self.frames[cont]
        frame.tkraise()

class Meeting(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame = Meeting
        self['background'] = '#fff8f0'

        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meeting), bg = "#9dd9d2").grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", command=lambda: controller.show_frame(Actions), bg = "#9dd9d2").grid(row = 0,column = 1)
        navbar_new_item = tk.Button(self, text="New Item", command=lambda: controller.show_frame(New_Item), bg = "#9dd9d2").grid(row = 0,column = 2)

        def select_item(item_name_selected):
            controller.show_frame(Item)
            row_num = cursor.execute("SELECT ROW_NUMBER() OVER (ORDER BY priority) row_num, item_name FROM items")
            #item_name = cursor.execute("SELECT item_name FROM items ORDER BY priority DESC")
            items = cursor.fetchall()
            print(item_name_selected)
            for row_num in items:
                print(row_num)
            item_selected = x-4
            return item_selected

        label = tk.Label(self, text="HYC Leadership Team Meeting", bg= '#fff8f0').grid(row=1, column=3, sticky=EW)
        label = tk.Label(self, text="Insert Meeting information", bg= '#fff8f0').grid(row=2, column=3, sticky=EW)
        label = tk.Label(self, text="Agenda:", bg= '#fff8f0').grid(row=3, column=3, sticky=EW)

        item_name = cursor.execute("SELECT item_name FROM items ORDER BY priority DESC")
        items = cursor.fetchall()
        x=4
        for item_name in items:
            open_pg_items = tk.Button(self, text=item_name, command=lambda: select_item(item_name))
            open_pg_items.grid(row = x,column = 4, columnspan=4, sticky=EW)
            x=x+1            

class Actions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self['background'] = '#fff8f0'
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meeting), bg = "#9dd9d2").grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", bg = "#9dd9d2").grid(row = 0,column = 1)
        navbar_new_action = tk.Button(self, text="New Action", command=lambda: controller.show_frame(New_Action), bg = "#9dd9d2").grid(row = 0,column = 2)
        label = tk.Label(self, text="Actions list").grid(row=1, column=4, columnspan=4) # Update when I know how many columns there will be

class New_Action(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def submit():
            controller.show_frame(Actions) 
            action_name1 = action_name_var.get()
            pic1 = pic_var.get()
            due1 = due_var.get()
            description1 = description_var.get()
            cursor.execute("select * from actions")
            cursor.execute("insert into actions values(%s, %s, %s, %s, %s)", (action_name1, pic1, due1, description1))
            conn.commit()
            action_name_var.delete(0, 'end')
            pic_var.delete(0, 'end')
            due_var.delete(0, 'end')
            description_var.delete(0, 'end')
            cursor.fetchall()

        navbar_actions = tk.Button(self, text="Back to Actions List", bg = "#9dd9d2", command=lambda: controller.show_frame(Actions)).grid(row = 0,column = 0, sticky=W)
        
        # New Action Form ~~~
        heading = tk.Label(self, text="Add a New Action", bg= '#fff8f0').grid(row=1, column=2, sticky=EW)
        action_name = tk.Label(self, text="Action Name", bg= '#fff8f0').grid(row=2, column=1, sticky=EW)
        action_name_var = ttk.Entry(self)
        action_name_var.grid(row=2, column=2, sticky=EW)
        pic = tk.Label(self, text="Person in Charge", bg= '#fff8f0').grid(row=3, column=1, sticky=EW) #make this a dropdown
        pic_var = ttk.Entry(self)
        pic_var.grid(row=3, column=2, sticky=EW)
        due = tk.Label(self, text="Due date", bg= '#fff8f0').grid(row=4, column=1, sticky=EW)
        due_var = ttk.Entry(self)
        due_var.grid(row=4, column=2, sticky=EW)
        description = tk.Label(self, text="Action Type", bg= '#fff8f0').grid(row=5, column=1, sticky=EW) #make this a dropdown
        description_var = ttk.Entry(self)
        description_var.grid(row=5, column=2, sticky=EW)
        add = tk.Button(self, text="Add Item to Agenda", bg="#ff8811", command=submit).grid(row=8, column=1)

class Item(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Item A")
        label.grid(row=1, column=3, columnspan=3)
        self['background'] = '#fff8f0'
        #navbar
        navbar_meetings = tk.Button(self, text="Back to Meeting", command=lambda: controller.show_frame(Meeting), bg = "#9dd9d2").grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", command=lambda: controller.show_frame(Actions), bg = "#9dd9d2").grid(row = 0,column = 1)
        navbar_new_action = tk.Button(self, text="New Action", command=lambda: controller.show_frame(New_Action), bg = "#9dd9d2").grid(row = 0,column = 2)
        label = tk.Label(self, text="Item information").grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

        item_name = cursor.execute("select item_name from items")
        priority = cursor.execute("select priority from items")
        item_des = cursor.execute("select item_des from items")
        action_type = cursor.execute("select action_type from items")
        est_time = cursor.execute("select est_time from items")
        items = cursor.fetchall()

        #Save button

class New_Item(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        def submit():
            controller.show_frame(Meeting) 
            item_name1 = item_name_var.get()
            priority1 = priority_var.get()
            item_des1 = item_des_var.get()
            action_type1 = action_type_var.get()
            est_time1 = est_time_var.get()
            cursor.execute("select * from items")
            cursor.execute("insert into items values(%s, %s, %s, %s, %s)", (item_name1, priority1, item_des1, action_type1, est_time1))
            conn.commit()
            item_name_var.delete(0, 'end')
            priority_var.delete(0, 'end')
            item_des_var.delete(0, 'end')
            action_type_var.delete(0, 'end')
            est_time_var.delete(0, 'end')
            cursor.fetchall()

        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meeting), bg = "#9dd9d2").grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", bg = "#9dd9d2").grid(row = 0,column = 1)
        navbar_new_action = tk.Button(self, text="New Action", command=lambda: controller.show_frame(New_Action), bg = "#9dd9d2").grid(row = 0,column = 2)

        # New Item Form ~~~
        heading = tk.Label(self, text="Add a New Item").grid(row=1, column=1)
        item_name = tk.Label(self, text="Item Name").grid(row=2, column=0)
        item_name_var = ttk.Entry(self)
        item_name_var.grid(row=2, column=1)
        priority = tk.Label(self, text="Priority").grid(row=3, column=0) #make this a dropdown
        priority_var = ttk.Entry(self)
        priority_var.grid(row=3, column=1)
        item_des = tk.Label(self, text="Item Description").grid(row=4, column=0)
        item_des_var = ttk.Entry(self)
        item_des_var.grid(row=4, column=1)
        action_type = tk.Label(self, text="Action Type").grid(row=5, column=0) #make this a dropdown
        action_type_var = ttk.Entry(self)
        action_type_var.grid(row=5, column=1)
        est_time = tk.Label(self, text="Estimated Time").grid(row=6, column=0)
        est_time_var = ttk.Entry(self)
        est_time_var.grid(row=6, column=1)
        add = ttk.Button(self, text="Add Item to Agenda", command=submit).grid(row=8, column=1)

if __name__ == "__main__":
    testObj = main()
    testObj.mainloop()