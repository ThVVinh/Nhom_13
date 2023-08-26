import tkinter as tk

class KeylogApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        
        self.title("Keystroke")
        self.geometry("350x350")
        
        self.txtKQ = tk.Text(self, state="disabled")
        self.txtKQ.place(x = 12, y = 77, width = 318, height = 182)

        self.button1 = tk.Button(self, text="Hook", command=self.hook)
        self.button1.place(x = 12, y = 12, width = 75, height = 59)

        self.button2 = tk.Button(self, text="Unhook", command=self.unhook)
        self.button2.place(x = 93, y = 13, width = 75, height = 58)

        self.button3 = tk.Button(self, text="In phím", command=self.log_keys)
        self.button3.place(x = 174, y = 12, width = 75, height = 59)

        self.butXoa = tk.Button(self, text="Xóa", command=self.clear)
        self.butXoa.place(x = 256, y = 13, width = 74, height = 58)

    def hook(self):
        pass  # Your code here
    
    def unhook(self):
        pass  # Your code here
    
    def log_keys(self):
        pass  # Your code here
    
    def clear(self):
        pass  # Your code here

if __name__ == "__main__":
    app = KeylogApp()
    app.mainloop()