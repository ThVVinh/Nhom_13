import tkinter as tk
from tkinter import ttk
import socket
import threading
from process_designer import ProcessApp
class Process(ProcessApp):
    def __init__(self, nw, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nw = nw  # Lưu giá trị self.nw
        self.client = client
        # Tạo widget Treeview
        self.tree = ttk.Treeview(self)
        self.process_info = None
        self.start_app = None
        self.protocol("WM_DELETE_WINDOW", self.on_close) 
    
    def update_tree(self, process_info):
        self.listView1.delete(*self.listView1.get_children())
        
        self.process_info = sorted(process_info, key=lambda info: info.split(', ')[0][6:])  # Sắp xếp theo tên

        for info in self.process_info:
            # Phân tích thông tin từ chuỗi
            parts = info.split(', ')
            name = parts[0][6:]  # Bỏ đi "Name: " ở đầu chuỗi
            pid = parts[1][5:]   # Bỏ đi "PID: " ở đầu chuỗi
            threads = parts[2][9:]  # Bỏ đi "Threads: " ở đầu chuỗi

            # Thêm thông tin vào cây
            self.listView1.insert("", "end", values=(name, pid, threads))

    def kill_process(self):
        selected_item = self.listView1.focus()  # Lấy phần tử đang được chọn
        if selected_item:
            item_data = self.listView1.item(selected_item, "values")  # Lấy dữ liệu của phần tử
            if item_data:
                pid = item_data[1]  # Lấy ID Process (PID)
                self.send_kill_command(pid)
                
                
    def send_kill_command(self, pid):
        message = f"KILL\nKILLID\n{pid}\n"
        self.nw.write(message)
        self.nw.flush()
        self.process_info = [info for info in self.process_info if not info.endswith(f"PID: {pid}")]
        self.update_tree(self.process_info)


    def view_process(self):
        self.nw.write("XEM\n")
        self.nw.flush()
        num_process_bytes = self.client.recv(4)
        num_process = int.from_bytes(num_process_bytes, byteorder='big')

        process_info = []
        for _ in range(num_process):
            info_length_bytes = self.client.recv(4)  # Nhận 4 bytes tiếp theo để biết độ dài của dữ liệu
            info_length = int.from_bytes(info_length_bytes, byteorder='big')
            
            info_bytes = self.client.recv(info_length)  # Nhận dữ liệu dựa vào độ dài đã nhận
            info = info_bytes.decode('utf-8')  # Chuyển bytes thành chuỗi văn bản
            process_info.append(info)
        self.update_tree(process_info)

    def start_process(self):
        start_dialog = tk.Toplevel(self)
        start_dialog.title("Start")
        start_dialog.geometry("284x51")

        def start_app():
            program_name = txtName.get()  # Lấy phần tử đang được nhập
            if program_name:
                self.send_start_command(program_name)

        butStart = ttk.Button(start_dialog, text="Start", command=start_app)
        butStart.place(x=197, y=10, width=75, height=23)

        txtName = tk.Entry(start_dialog)
        txtName.insert(0, "Nhập tên")
        txtName.place(x=25, y=13, width=155, height=20)

        start_dialog.mainloop()
                
    def send_start_command(self, program_name):
        message = f"START\nSTARTID\n{program_name}\n"
        self.nw.write(message)
        self.nw.flush()

    def delete_process(self):
        self.listView1.delete(*self.listView1.get_children())
        
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
