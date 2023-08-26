import tkinter as tk
from tkinter import messagebox
from socket import socket, AF_INET, SOCK_STREAM
from listApp import ListAppProcess  # Import the corresponding Python file for listApp
from registry import RegistryProcess  # Import the corresponding Python file for registry
from keylog import KeylogProcess # Import the corresponding Python file for keylog
from client_designer import ClientDesignerApp
from pic import PicProcess
from process import Process

class ClientApp(ClientDesignerApp):
    def butConnect_Click(self):
        try:
            ip_address = self.txtIP.get()
            Program.client = socket(AF_INET, SOCK_STREAM)
            Program.client.connect((ip_address, 5656))
            Program.ns = Program.client.makefile("rw") # tạo một đối tượng luồng (stream) để gửi và nhận dữ liệu giữa client và server thông qua socket đã thiết lập
            Program.nw = Program.ns
            
            message = "CONNECTED\n"
            Program.ns.write(message)
            Program.nw.flush()
            messagebox.showinfo("Success", "Connected to server successfully")
        except OSError as ex:
            messagebox.showerror("Error", "Failed to connect to server")

    def butApp_Click(self):
        if Program.client:
            Program.nw.write("APPLICATION\n")
            Program.nw.flush()
            viewApp = ListAppProcess(Program.nw, Program.client)
            viewApp.mainloop()
            
    def butProcess_Click(self):
        if Program.client:
            Program.nw.write("PROCESS\n")
            Program.nw.flush()
            viewApp = Process(Program.nw, Program.client)
            viewApp.mainloop()

    def butReg_Click(self):
        if Program.client:
            Program.nw.write("REGISTRY\n")
            Program.nw.flush()
            viewApp = RegistryProcess(Program.nw, Program.client)
            viewApp.mainloop()

    def butExit_Click(self):
        if Program.client:
            Program.nw.write("QUIT\n")
            Program.nw.flush()
            self.destroy()

    def butPic_Click(self):
        if Program.client:
            Program.nw = Program.client.makefile("rw")
            Program.nw.write("TAKEPIC\n")
            Program.nr = Program.client.makefile("r")
            ViewApp = PicProcess(Program.nw, Program.client)
            ViewApp.mainloop()

    def butKeyLock_Click(self):
        if Program.client:
            Program.nw.write("KEYLOG\n")
            Program.nw.flush()
            ViewApp = KeylogProcess(Program.nw, Program.client)
            ViewApp.mainloop()
        
    def butShutdown_Click(self):
        if Program.client:
            Program.nw.write("SHUTDOWN\n")
            Program.nw.flush()

if __name__ == "__main__":
    Program = lambda: None
    Program.client = None
    Program.nw = None
    app = ClientApp()
    app.mainloop()