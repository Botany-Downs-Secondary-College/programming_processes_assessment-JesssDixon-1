from asyncio.windows_events import NULL
import tkinter as tk

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
        container = tk.Frame(self, height=4000, width=6000)
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
        
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings")
        navbar_meetings.grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions", command=lambda: controller.show_frame(Actions))
        navbar_actions.grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting))
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
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting))
        navbar_new_meeting.grid(row = 0,column = 2)
        navbar_new_item = tk.Button(self, text="New Item", command=lambda: controller.show_frame(New_Item))
        navbar_new_item.grid(row = 0,column = 3)

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
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting))
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
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting))
        navbar_new_meeting.grid(row = 0,column = 2)

        label = tk.Label(self, text="Items List")
        label.grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

class New_Item(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meetings))
        navbar_meetings.grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions")
        navbar_actions.grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting))
        navbar_new_meeting.grid(row = 0,column = 2)

        # New Item Form ~~~
        heading = tk.Label(text="Add a New Item")
        heading.grid(row=0, column=1)

        item_name = tk.Label(text="Item Name")
        item_name.grid(row=1, column=0)
        item_name_var = tk.Entry(root)
        item_name_var.grid(row=1, column=1)

        priority = tk.Label(text="Priority") #make this a dropdown
        priority.grid(row=2, column=0)
        priority_var = tk.Entry(root)
        priority_var.grid(row=2, column=1)

        item_des = tk.Label(text="Item Description")
        item_des.grid(row=3, column=0)
        item_des_var = tk.Entry(root)
        item_des_var.grid(row=3, column=1)

        action_type = tk.Label(text="Action Type") #make this a dropdown
        action_type.grid(row=4, column=0)
        action_type_var = tk.Entry(root)
        action_type_var.grid(row=4, column=1)

        est_time = tk.Label(text="Estimated Time")
        est_time.grid(row=5, column=0)
        est_time_var = tk.Entry(root)
        est_time_var.grid(row=5, column=1)
    
        # create a Submit Button and place into the root window
        #add = tk.Button(root, text="Add Item to Agenda", fg="Black", command=)
        #add.grid(row=8, column=1)
        
 
        #label.grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

class New_Meeting(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #navbar
        navbar_meetings = tk.Button(self, text="My Meetings", command=lambda: controller.show_frame(Meetings))
        navbar_meetings.grid(row = 0,column = 0)
        navbar_actions = tk.Button(self, text="Actions")
        navbar_actions.grid(row = 0,column = 1)
        navbar_new_meeting = tk.Button(self, text="New Meeting", command=lambda: controller.show_frame(New_Meeting))
        navbar_new_meeting.grid(row = 0,column = 2)

        label = tk.Label(self, text="Actions list")
        label.grid(row=1, column=3, columnspan=3) # Update when I know how many columns there will be

if __name__ == "__main__":
    testObj = main()
    testObj.mainloop()