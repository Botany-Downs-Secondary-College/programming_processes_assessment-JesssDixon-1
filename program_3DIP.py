"""
Jessica Dixon 2022
Agenda Writing Application
Developed for the Howick Youth Council
"""
# importing required modules
# tkinter modules
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import Tk, font
from tkinter import messagebox
# timing
import datetime
import sys
import time
# pdf
from reportlab.pdfgen import canvas

# connecting code with SQL database
import psycopg2
conn = psycopg2.connect(database="agenda_info",
                        user="postgres",
                        password="1234",
                        host="127.0.0.1",
                        port="5432")
cursor = conn.cursor()

# initialising global variables
selected_item = [""]
count = 0
s = 0
m = 0
h = 0
start_mins = 0


class main(tk.Tk):
    def __init__(main, *args, **kwargs):
        tk.Tk.__init__(main, *args, **kwargs)
        # Window setup
        main.title("Meeting Agenda")
        main['background'] = '#fff8f0'
        width = main.winfo_screenwidth()  # gets dimensions of user's screen
        height = main.winfo_screenheight()
        main.geometry("%dx%d" % (width, height))

        # Navigation mechanism setup
        container = tk.Frame(main)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Using a method to switch frames
        main.frames = {}
        for page in (Meeting, Actions, New_Action, New_Item):
            frame = page(container, main)
            main.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        main.show_frame(Meeting)

    def show_frame(self, cont):  # raises frame to top
        frame = self.frames[cont]
        re_cont = Frame(self)
        frame.tkraise()


class Meeting(tk.Frame):
    def start(self):
        global count
        count = 0
        ans = messagebox.askquestion("askquestion",
                                     """Make sure you have added all agenda items before you start the meeting.
                                     Are you ready to start the meeting?""")
        if ans == 'yes':
            self.timer()

    def timer(self):
        global count
        global s
        global m
        global h
        if count == 0:
            self.d = str(self.t.get())
            h, m, s = map(int, self.d.split(":"))
            h = int(h)
            m = int(m)
            s = int(s)
            if s < 59:
                s += 1
            elif s == 59:
                s = 0
                if m < 59:
                    m += 1
                elif m == 59:
                    m = 0
                    h += 1
            if h < 10:
                h = str(0) + str(h)
            else:
                h = str(h)
            if m < 10:
                m = str(0) + str(m)
            else:
                m = str(m)
            if s < 10:
                s = str(0) + str(s)
            else:
                s = str(s)
            self.d = h + ":" + m + ":" + s
            self.t.set(self.d)
            if count == 0:
                self.after(1000, self.timer)

    def __init__(Meeting, parent, controller):
        tk.Frame.__init__(Meeting, parent)
        Meeting['background'] = '#fff8f0'
        Meeting.defaultFont = font.nametofont("TkDefaultFont")
        Meeting.defaultFont.configure(family="Yu Gothic", size=11)

        def end_meeting():
            main.quit(Meeting)
            cursor.execute(
                "SELECT item_name FROM items ORDER BY item_name DESC")
            item_names = cursor.fetchall()
            cursor.execute(
                "SELECT priority FROM items ORDER BY item_name DESC")
            priorities = cursor.fetchall()
            cursor.execute(
                "SELECT item_des FROM items ORDER BY item_name DESC")
            item_dess = cursor.fetchall()
            cursor.execute(
                "SELECT act_time FROM items ORDER BY item_name DESC")
            times = cursor.fetchall()
            cursor.execute(
                "SELECT minutes FROM items ORDER BY item_name DESC")
            minutess = cursor.fetchall()
            # remove finished items from SQL
            day = datetime.datetime.now()
            d = day.strftime("%d")
            b = day.strftime("%b")
            title = (d + " " + b +
                     """ Howick Youth Council Meeting Leadership Team Minutes""")
            filename = title + ".pdf"
            pdf = canvas.Canvas(filename)
            pdf.setTitle(title)
            pdf.drawString(130, 770, title)
            pdf.drawString(250, 750, "Agenda Items:")
            a = 0
            y = 720
            x = 20
            for item in item_names:
                item_name = str(item_names[a]).strip("()'',")
                priority = str(priorities[a]).strip("()'',")
                item_des = str(item_dess[a]).strip("()'',")
                time = str(times[a]).strip("()'',")
                minutes = str(minutess[a]).strip("()'',")
                if minutes != "Not yet discussed":
                    commandline = "DELETE FROM items WHERE item_name = '{}'".format(item_name)
                    cursor.execute(commandline)
                    conn.commit()
                pdf.drawString(x, y, item_name + " (Priority: " + priority +
                               ", Time Spent: " + time + ") :" + item_des)
                pdf.drawString(x, y-20, minutes)
                a = a + 1
                y = y - 50

            cursor.execute(
                "SELECT action_name FROM actions ORDER BY action_name DESC")
            action_names = cursor.fetchall()
            cursor.execute(
                "SELECT pic FROM actions ORDER BY action_name DESC")
            pics = cursor.fetchall()
            cursor.execute(
                "SELECT due FROM actions ORDER BY action_name DESC")
            dues = cursor.fetchall()
            cursor.execute(
                "SELECT description FROM actions ORDER BY action_name DESC")
            descriptions = cursor.fetchall()
            cursor.execute(
                "SELECT done FROM actions ORDER BY action_name DESC")
            dones = cursor.fetchall()

            pdf.drawString(270, y, "Actions:")
            y = y - 20
            a = 0
            x = 20
            for action in action_names:
                action_name = str(action_names[a]).strip("()'',")
                pic = str(pics[a]).strip("()'',")
                due = str(dues[a]).strip("()'',")
                description = str(descriptions[a]).strip("()'',")
                done = str(dones[a]).strip("()'',")
                if done == 'Done':
                    commandline = "DELETE FROM actions WHERE action_name = '{}'".format(action_name)
                    cursor.execute(commandline)
                    conn.commit()
                pdf.drawString(x, y, action_name + " (Priority: " + pic +
                               ", Time Spent: " + due + ") :" + description)
                pdf.drawString(x, y-20, done)
                a = a + 1
                y = y - 50
            pdf.save()

        # navbar
        Meeting.t = StringVar()
        Meeting.t.set("00:00:00")
        navbar_actions = tk.Button(Meeting, text="Actions",
                                   command=lambda: controller.show_frame(Actions),
                                   bg="#9dd9d2", width=10)
        navbar_actions.grid(row=0, column=0, sticky=NW)
        navbar_new_item = tk.Button(Meeting, text="New Item",
                                    command=lambda: controller.show_frame(New_Item),
                                    bg="#9dd9d2", width=10)
        navbar_new_item.grid(row=0, column=1, sticky=NW)
        start_meeting_btn = tk.Button(Meeting, text="Start Timer",
                                      command=Meeting.start, bg="#9dd9d2", width=10)
        start_meeting_btn.grid(row=0, column=2, sticky=NW)
        timer_display = tk.Button(Meeting, textvariable=Meeting.t, width=10,
                                  bg="#392F5A", fg="#FFF8F0")
        timer_display.grid(row=0, column=3, sticky=NW)
        end_meeting_btn = tk.Button(Meeting, text="End Meeting",
                                    command=end_meeting, bg="#9dd9d2", width=10)
        end_meeting_btn.grid(row=0, column=4, sticky=NW)

        def selection(a):  # selects what item the user chose
            global selected_item
            global m
            global h
            global start_mins
            start_mins = (int(s)/60) + int(m) + (int(h)*60)
            del selected_item[0]
            selected_item.append(a)
            item_chosen.set(str(selected_item[0]).strip("()'',"))
            sql1 = "SELECT item_des FROM items WHERE item_name = %s"
            sql2 = "SELECT est_time FROM items WHERE item_name = %s"
            sql3 = "SELECT minutes FROM items WHERE item_name = %s"
            a = (selected_item[0])
            cursor.execute(sql1, a)
            item_des = cursor.fetchall()
            cursor.execute(sql2, a)
            est_time = cursor.fetchall()
            cursor.execute(sql3, a)
            mins = cursor.fetchall()
            item_des = str(item_des).strip("\{\}()'',[]")
            est_time = str(est_time).strip("[]()'',")
            mins = str(mins).strip("[]()'',")
            item_des_a.set(item_des)
            est_time_format = "Estimated Time: {} minutes".format(est_time)
            est_time_a.set(est_time_format)
            if mins != "Not yet discussed":
                minutes.delete('1.0', END)
                minutes.insert(INSERT, mins)
            else:
                minutes.delete('1.0', END)
                minutes.insert(INSERT,
                               "Record minutes here. Remember to press \"Save\" when you\'re done!")

        # List of Agenda Items
        items_dict = {}
        cursor.execute("SELECT item_name FROM items ORDER BY priority DESC")
        items = cursor.fetchall()  # get data from SQL table
        x = 2  # start count of rows at 3 to allow for navigation bar and titles
        label = Label(Meeting, text="Agenda Items", bg="#FFF8F0", pady=10, font="bahnschrift")
        label.grid(row=1, column=0, columnspan=5)
        for item in items:
            # pass each button's text to a function
            def select_item(x=item):
                return selection(x)
            items_dict[item] = tk.Button(Meeting, text=str(item).strip("()'',"), width=50, command=select_item, bg="#F4D06F")
            items_dict[item].grid(row=x, column=0, columnspan=5)  # sets button command to function
            x = x + 1  # new row

        def Save():
            global m
            global h
            global start_mins
            end_mins = (int(s)/60) + int(m) + (int(h)*60)
            time = int(end_mins) - int(start_mins)
            minutes1 = minutes.get(1.0, "end-1c")
            cursor.execute("SELECT * FROM items")
            cursor.execute("UPDATE items SET minutes = %s WHERE item_name = %s", (minutes1, selected_item[0]))
            cursor.execute("UPDATE items SET act_time = %s WHERE item_name = %s", (time, selected_item[0]))
            conn.commit()

        # Agenda Item and Minutes
        item_chosen = StringVar()  # Defines variable type for item_chosen
        infor = StringVar()
        item_des_a = StringVar()
        est_time_a = StringVar()
        label1 = tk.Label(Meeting, text="HYC Leadership Team Meeting", bg='#fff8f0', font=('Bahnschrift', 20)).grid(row=0, column=6)
        item_chosen.set("Agenda item information will appear here")
        label = Label(Meeting, textvariable=item_chosen, bg="#FFF8F0").grid(row=1, column=6)
        item_des_a.set("Select an item to the left to get started")
        label = Label(Meeting, textvariable=item_des_a, bg="#FFF8F0").grid(row=2, column=6)
        est_time_a.set("Remember to save your minutes before moving on to another item")

        label = Label(Meeting, textvariable=est_time_a, bg="#FFF8F0").grid(row=3, column=6)
        save = Button(Meeting, text="Save Minutes", command=Save, bg="#FF8811")
        save.grid(row=4, column=6)
        minutes = tk.Text(Meeting, bg="#FFF8F0", font="bahnschrift", width=82, height=23)
        minutes.insert(INSERT, "Record minutes here. Remember to press \"Save\" when you\'re done!")
        minutes.grid(row=5, column=6, rowspan=100)


class Actions(tk.Frame):
    def __init__(Actions, parent, controller):
        tk.Frame.__init__(Actions, parent)
        Actions['background'] = '#fff8f0'
        # navigation bar
        navbar_meetings = tk.Button(Actions, text="Back to Meeting", command=lambda: controller.show_frame(Meeting), bg="#9dd9d2").grid(row=0,column=0)
        navbar_new_action = tk.Button(Actions, text="New Action", command=lambda: controller.show_frame(New_Action), bg="#9dd9d2").grid(row=0,column=1)
        label = tk.Label(Actions, text="Actions list", bg="#FFF8F0", font=('Bahnschrift', 20)).grid(row=1, column=2, columnspan=5)

        actions_dict = {}
        action_name = cursor.execute("SELECT * FROM actions ORDER BY pic DESC")
        actions = cursor.fetchall()
        actions.insert(0, ("Action", "Person in Charge", "Due Date", "Description", "Status"))

        def done(x):
            action_name = action_names[x]
            cursor.execute("UPDATE actions SET done = %s WHERE action_name = %s", ("Done", action_name))
            conn.commit()

        bord = "groove"
        action_names = {}
        total_rows = len(actions)
        for row in range(total_rows):
            if row == 0:
                backg = "#392F5A"
                forg = "#FFF8F0"
            else:
                backg = "#FFF8F0"
                forg = "black"
            for column in range(5):
                if column == 0:
                    action_names[row] = actions[row][column]
                    tbl = Label(Actions, text=actions[row][column], width=20, bg=backg, fg=forg, borderwidth=2, relief=bord, height=2)
                if column == 4:
                    if row == 0:
                        tbl = Label(Actions, text="Mark Complete", width=20, bg=backg, fg=forg, borderwidth=2, relief=bord, height=2)
                    else:
                        def done_action(x=row):
                            return done(x)
                        tbl = Button(Actions, text="Mark as complete", command=done_action, bg="#F4D06F", width=20, borderwidth=2, relief=bord, height=2)
                else:
                    tbl = Label(Actions, text=actions[row][column], width=20, bg=backg, fg=forg, borderwidth=2, relief=bord, height=2)
                tbl.grid(row=row+2, column=column+2)


class New_Action(tk.Frame):
    def __init__(New_Action, parent, controller):
        tk.Frame.__init__(New_Action, parent)
        New_Action['background'] = '#fff8f0'

        def submit():
            action_name1 = action_name_var.get()
            pic1 = pic_var.get()
            due1 = due_var.get()
            description1 = description_var.get()
            cursor.execute("SELECT * FROM actions")
            cursor.execute("INSERT INTO actions VALUES(%s, %s, %s, %s, %s)", (action_name1, pic1, due1, description1, "In Progress"))
            conn.commit()
            action_name_var.delete(0, 'end')
            pic_var.delete(0, 'end')
            due_var.delete(0, 'end')
            description_var.delete(0, 'end')

        navbar_actions = tk.Button(New_Action, text="Back to Actions", bg="#9dd9d2", command=lambda: controller.show_frame(Actions)).grid(row=0,column=0, sticky=W)

        # New Action Form
        heading = tk.Label(New_Action, text="Add a New Action", bg='#fff8f0', font=("bahnschrift", 20), width=50).grid(row=1, column=2, sticky=EW)
        action_name = tk.Label(New_Action, text="Action Name", bg='#fff8f0').grid(row=2, column=1, sticky=EW)
        action_name_var = tk.Entry(New_Action, fg='#fff8f0', bg="#392F5A")
        action_name_var.grid(row=2, column=2, sticky=EW, ipady=5)
        pic = tk.Label(New_Action, text="Person in Charge", bg='#fff8f0').grid(row=3, column=1, sticky=EW)
        pic_var = tk.Entry(New_Action, width= 70, fg='#fff8f0', bg="#392F5A")
        pic_var.grid(row=3, column=2, sticky=EW, ipady=5)
        due = tk.Label(New_Action, text="Due date", bg= '#fff8f0').grid(row=4, column=1, sticky=EW)
        due_var = tk.Entry(New_Action, fg='#fff8f0', bg="#392F5A")
        due_var.grid(row=4, column=2, sticky=EW, ipady=5)
        description = tk.Label(New_Action, text="Description", bg= '#fff8f0').grid(row=5, column=1, sticky=EW)
        description_var = tk.Entry(New_Action, fg='#fff8f0', bg="#392F5A")
        description_var.grid(row=5, column=2, sticky=EW, ipady=5)
        add = tk.Button(New_Action, text="Add Action", bg="#ff8811", command=submit).grid(row=8, column=2)


class New_Item(tk.Frame):
    def __init__(New_Item, parent, controller):
        tk.Frame.__init__(New_Item, parent)
        New_Item['background'] = '#fff8f0'

        def submit():
            err = False
            item_name1 = item_name_var.get()
            try:
                priority1 = int(priority_var.get())
            except:
                error = tk.Label(New_Item, text="Error: Priority must be an integer")
                error.grid(row=9, column=1)
                err = True
            item_des1 = item_des_var.get()
            try:
                est_time1 = int(est_time_var.get())
            except:
                error = tk.Label(New_Item, text="Error: Estimated Time must be an integer", bg='#fff8f0')
                error.grid(row=9, column=2)
                err = True
            if err == False:
                cursor.execute("SELECT * FROM items")
                cursor.execute("INSERT INTO items VALUES(%s, %s, %s, %s, %s, %s)",
                                (item_name1, priority1, item_des1, est_time1, 0, "Not yet discussed"))
                conn.commit()
                item_name_var.delete(0, 'end')
                priority_var.delete(0, 'end')
                item_des_var.delete(0, 'end')
                est_time_var.delete(0, 'end')

        # Navigation bar
        navbar_meetings = tk.Button(New_Item, text="Back to Meeting", command=lambda: controller.show_frame(Meeting), bg="#9dd9d2").grid(row=0, column=0)

        # New Item Form
        heading = tk.Label(New_Item, text="Add a New Item", bg='#fff8f0', font=("bahnschrift", 20)).grid(row=1, column=2)
        item_name = tk.Label(New_Item, text="Item Name", bg='#fff8f0').grid(row=2, column=1)
        item_name_var = tk.Entry(New_Item, fg='#fff8f0', bg="#392F5A", width=70)
        item_name_var.grid(row=2, column=2, ipady=5)
        priority = tk.Label(New_Item, text="Priority (scale of 1-10)", bg='#fff8f0').grid(row=3, column=1)
        priority_var = tk.Entry(New_Item, fg='#fff8f0', bg="#392F5A", width=70)
        priority_var.grid(row=3, column=2, ipady=5)
        item_des = tk.Label(New_Item, text="Item Description", bg='#fff8f0').grid(row=4, column=1)
        item_des_var = tk.Entry(New_Item, fg='#fff8f0', bg="#392F5A", width=70)
        item_des_var.grid(row=4, column=2, ipady=5)
        est_time = tk.Label(New_Item, text="Estimated Time (in minutes)", bg='#fff8f0').grid(row=6, column=1)
        est_time_var = tk.Entry(New_Item, fg='#fff8f0', bg="#392F5A", width=70)
        est_time_var.grid(row=6, column=2, ipady=5)
        add = tk.Button(New_Item, text="Add Item to Agenda", command=submit, bg='#ff8811').grid(row=8, column=2)

if __name__ == "__main__":  # main routine
    routine = main()
    routine.mainloop()
