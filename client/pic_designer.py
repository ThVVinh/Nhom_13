import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

class PicDesigner(tk.Toplevel):
    def __init__(self):
        # pic
        super().__init__()
        self.title("Pic")
        self.geometry("500x400")
        
        #picture
        self.picture = tk.Label(self)
        self.picture.place(x=12, y=12, width=400, height=400)
        
        #butTake
        self.butTake = ttk.Button(self, text="Chụp", command=self.take_picture)
        self.butTake.place(x=420, y=12, width=75, height=175)
        
        #button1
        self.button1 = ttk.Button(self, text="Lưu", command=self.save_picture)
        self.button1.place(x=420, y=209, width=75, height=175)
        
        self.saveFileDialog = filedialog.SaveAs(self)
        
        
    
    def take_picture(self):
        pass
    
    def save_picture(self):
        pass

    