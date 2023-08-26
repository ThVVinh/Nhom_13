import tkinter as tk
from tkinter import DISABLED, ttk

class RegistryApp(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Registry")
        self.geometry("415x380")
        
        self.txtBro = tk.Entry(self)
        self.txtBro.insert(0, "Đường dẫn ...")
        self.txtBro.place(x=2, y=23, width=311, height=20)
        
        self.butBro = ttk.Button(self, text="Browser...", command=self.butBro_Click)
        self.butBro.place(x=319, y=20, width=90, height=23)
        
        self.txtReg = tk.Text(self)
        self.txtReg.insert(tk.END, "Nội dung")
        self.txtReg.place(x=2, y=55, width=311, height=77)
        
        self.butSend = ttk.Button(self, text="Gửi nội dung", command=self.butSend_Click)
        self.butSend.place(x=319, y=55, width=90, height=77)
        
        self.groupBox1 = ttk.LabelFrame(self, text="Sửa giá trị trực tiếp")
        self.groupBox1.place(x=2, y=138, width=405, height=225)
        
        self.opApp = ttk.Combobox(self.groupBox1, values=["Get value", "Set value", "Delete value", "Create key", "Delete key"])
        self.opApp.set("Chọn chức năng")
        self.opApp.place(x=6, y=19, width=372)
        self.opApp.bind("<<ComboboxSelected>>", self.comboBox2_SelectedIndexChanged)

        self.txtKQ = tk.Text(self.groupBox1, state=DISABLED)
        self.txtKQ.insert("1.0", "")
        self.txtKQ.place(x=6, y=99, width=372, height=68)
        
        self.txtLink = tk.Entry(self.groupBox1)
        self.txtLink.insert(0, "Đường dẫn")
        self.txtLink.place(x=6, y=46, width=372, height=20)
        
        self.txtNameValue = tk.Entry(self.groupBox1)
        self.txtNameValue.insert(0, "Name value")
        self.txtNameValue.place(x=6, y=72, width=113, height=20)
        
        self.txtValue = tk.Entry(self.groupBox1)
        self.txtValue.insert(0, "Value")
        self.txtValue.place(x=125, y=72, width=138, height=20)
        
        self.opTypeValue = ttk.Combobox(self.groupBox1, values=["String", "Binary", "DWORD", "QWORD", "Multi-String", "Expandable String"])
        self.opTypeValue.set("Type")
        self.opTypeValue.place(x=269, y=72, width=109, height=21)
        
        self.button1 = ttk.Button(self.groupBox1, text="Gửi", command=self.button1_Click)
        self.button1.place(x=69, y=173, width=97, height=23)
        
        self.butXoa = ttk.Button(self.groupBox1, text="Xóa", command=self.delete_value)
        self.butXoa.place(x=192, y=173, width=94, height=23)

    def butSend_Click(self):
        # Your logic for sending content goes here
        pass
        
    def butBro_Click(self):
        pass

        
    def button1_Click(self):
        # Your logic for sending direct value goes here
        pass
    
    def comboBox2_SelectedIndexChanged(self, event):
        # Your logic for sending direct value goes here
        pass
        
    def delete_value(self):
        # Your logic for deleting value goes here
        pass

if __name__ == "__main__":
    app = RegistryApp()
    app.mainloop()
