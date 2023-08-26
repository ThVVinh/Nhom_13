import tkinter as tk

class ClientDesignerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Client")
        self.geometry("375x275") #Đặt kích thước cho cửa sổ
        
        self.butApp = tk.Button(self, text="App Running", command=self.butApp_Click) #tạo button
        self.butApp.place(x=118, y=64, width=145, height=63) # đặt vị trí và kích thước
        
        self.butConnect = tk.Button(self, text="Kết nối", command=self.butConnect_Click)
        self.butConnect.place(x=244, y=27, width=125, height=23)

        self.txtIP = tk.Entry(self)
        self.txtIP.insert(0, "Nhập IP") #placeholder
        self.txtIP.place(x=12, y=29, width=226, height=20)
        

        self.butTat = tk.Button(self, text="Tắt máy", command=self.butShutdown_Click)
        self.butTat.place(x=118, y=133, width=48, height=57)
        

        self.butReg = tk.Button(self, text="Sửa registry", command=self.butReg_Click)
        self.butReg.place(x=118, y=196, width=198, height=65)
       

        self.butExit = tk.Button(self, text="Thoát", command=self.butExit_Click)
        self.butExit.place(x=322, y=196, width=47, height=65)
        

        self.butPic = tk.Button(self, text="Chụp màn hình", command=self.butPic_Click)
        self.butPic.place(x=173, y=133, width=91, height=57)
        

        self.butKeyLock = tk.Button(self, text="Keystroke", command=self.butKeyLock_Click)
        self.butKeyLock.place(x=269, y=64, width=100, height=126)
        

        self.butProcess = tk.Button(self, text="Process Running", command=self.butProcess_Click)
        self.butProcess.place(x=12, y=64, width=100, height=197)
        

    def butApp_Click(self):
        pass  # Your code here
    
    def butConnect_Click(self):
        pass  # Your code here
    
    def butShutdown_Click(self):
        pass  # Your code here
    
    def butReg_Click(self):
        pass  # Your code here
    
    def butExit_Click(self):
        pass
    
    def butPic_Click(self):
        pass  # Your code here
    
    def butKeyLock_Click(self):
        pass  # Your code here
    
    def butProcess_Click(self):
        pass  # Your code here