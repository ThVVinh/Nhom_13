import tkinter as tk
from tkinter import ttk

class ListApp(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("List App")
        self.geometry("330x300")

        self.button2 = tk.Button(self, text="Kill", command=self.kill_application)
        self.button2.place(x=22, y=12, width=64, height=52)
        
        self.button1 = tk.Button(self, text="Xem", command=self.view_application)
        self.button1.place(x=92, y=12, width=65, height=52)
  
        self.button4 = tk.Button(self, text="Xóa", command=self.delete_application)
        self.button4.place(x=163, y=12, width=75, height=52)

        self.button3 = tk.Button(self, text="Start", command=self.start_application)
        self.button3.place(x=244, y=12, width=64, height=52)

        #listView
        self.columns = ("Name Application", "ID Application", "Count Thread") #danh sách các cột
        self.listView1 = ttk.Treeview(self, columns=self.columns, show="headings") #tạo widget
        
        self.listView1.heading("Name Application", text="Name Application") #đặt tiêu đề cho mỗi cột
        self.listView1.column("Name Application", width=96) # đặt chiều rộng mỗi cột
        
        self.listView1.heading("ID Application", text="ID Application") #đặt tiêu đề cho mỗi cột
        self.listView1.column("ID Application", width=100) # đặt chiều rộng mỗi cột
        
        self.listView1.heading("Count Thread", text="Count Thread") #đặt tiêu đề cho mỗi cột
        self.listView1.column("Count Thread", width=82) # đặt chiều rộng mỗi cột
        
        self.listView1.place(x=22, y=83, width=286, height=182)

    def view_application(self):
        # Code to populate the list of applications
        pass

    def kill_application(self):
        pass

    def start_application(self):
        # Code to start the selected application
        pass

    def delete_application(self):
        pass

if __name__ == "__main__":
    app = ListApp()
    app.mainloop()
