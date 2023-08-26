import tkinter as tk
from tkinter import ttk

class ProcessApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("List Process")
        self.geometry("302x261")
        
        self.button1 = ttk.Button(self, text="Kill", command=self.kill_process)
        self.button1.place(x=24, y=12, width=66, height=47)
        
        self.button2 = ttk.Button(self, text="Xem", command=self.view_process)
        self.button2.place(x=96, y=12, width=59, height=47)
        
        self.button3 = ttk.Button(self, text="Start", command=self.start_process)
        self.button3.place(x=231, y=12, width=59, height=47)
        
        self.button4 = ttk.Button(self, text="Xóa", command=self.delete_process)
        self.button4.place(x=161, y=12, width=64, height=47)
        
        self.listView1 = ttk.Treeview(self, columns=("Name Process", "ID Process", "Count Thread"), show="headings")
        self.listView1.heading("Name Process", text="Name Process")
        self.listView1.column("Name Process", width=100)
        self.listView1.heading("ID Process", text="ID Process")
        self.listView1.column("ID Process", width=65)
        self.listView1.heading("Count Thread", text="Count Thread")
        self.listView1.column("Count Thread", width=75)
        self.listView1.place(x=24, y=74, width=266, height=162)
        

    def kill_process(self):
        # Your logic for killing a process goes here
        pass
        
    def view_process(self):
        # Your logic for viewing processes goes here
        pass
        
    def start_process(self):
        # Your logic for starting a process goes here
        pass
        
    def delete_process(self):
        # Your logic for deleting a process goes here
        pass

if __name__ == "__main__":
    app = ProcessApp()
    app.mainloop()