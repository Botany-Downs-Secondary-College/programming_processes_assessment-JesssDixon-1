import tkinter as tk
from tkinter import BOTH, LEFT, ttk

root = tk.Tk()
def createNewWindow():
    newWindow = tk.Toplevel(root)
    labelExample = tk.Label(newWindow, text = "New Window")
    buttonExample = tk.Button(newWindow, text = "New Window button")

    labelExample.pack()
    buttonExample.pack()

class main(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("App Name")
        container = tk.Frame(self, height=400, width=600)
        container.grid(row = 0,column = 0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for page in (Meetings, MeetingX, Item, Actions):
            frame = page(container, self)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Meetings)

    def show_frame(self, cont): #raises frame to top
        frame = self.frames[cont]
        frame.tkraise()

class Meetings(tk.Frame):
    buttonExample = tk.Button(root, text="PLEASEEEEEEEEEEEEEEEEE", command=createNewWindow)
    buttonExample.pack()
    
    def __init__(self, parent, controller):     
        tk.Frame.__init__(self, parent)
        
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings")
        navbar_meetings.grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", command=lambda: controller.show_frame(Actions))
        navbar_actions.grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting")
        navbar_new_meeting.grid(row = 0,column = 2)

        label = tk.Label(self, text="App name")
        label.grid(row=1, column=2, columnspan=3) # Update when I know how many columns there will be

        # Meeting list - this should become a for loop that prints meeting details for each meeting
        open_pg_meeting = tk.Button(self, text="Meeting X", command=lambda: controller.show_frame(MeetingX))
        open_pg_meeting.grid(row = 3,column = 3)

class MeetingX(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Meeting XYZ")
        label.grid(row=1, column=3, columnspan=3)

        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meetings))
        navbar_meetings.grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", command=lambda: controller.show_frame(Actions))
        navbar_actions.grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting")
        navbar_new_meeting.grid(row = 0,column = 2)

        label = tk.Label(self, text="Items List")
        label.grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

        #Item list - this should become a for loop that prints meeting details for each meeting
        open_pg_items = tk.Button(self, text="Item", command=lambda: controller.show_frame(Item))
        open_pg_items.grid(row = 2,column = 2)

class Actions(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meetings))
        navbar_meetings.grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions")
        navbar_actions.grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting")
        navbar_new_meeting.grid(row = 0,column = 2)

        label = tk.Label(self, text="Actions list")
        label.grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

class Item(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Item A")
        label.grid(row=1, column=3, columnspan=3)

        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meetings))
        navbar_meetings.grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", command=lambda: controller.show_frame(Actions))
        navbar_actions.grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting")
        navbar_new_meeting.grid(row = 0,column = 2)

        label = tk.Label(self, text="Items List")
        label.grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

if __name__ == "__main__":
    testObj = main()
    testObj.mainloop()