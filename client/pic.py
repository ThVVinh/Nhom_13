import tkinter as tk
from tkinter import filedialog
from pic_designer import PicDesigner
from mss import mss
import threading
from PIL import Image, ImageTk
import io



class PicProcess(PicDesigner):
    def __init__(self, nw, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nw = nw  # Lưu giá trị self.nw
        self.client = client
        self.img_tk = None
        self.screenshot_data = None
        self.protocol("WM_DELETE_WINDOW", self.on_close) 
        
    def take_picture(self):
        # Kiểm tra trạng thái chụp
            self.is_taking_picture = True
            self.nw.write("TAKE\n")
            self.nw.flush()
            
            # Tạo một luồng để nhận dữ liệu hình ảnh từ server
            receive_thread = threading.Thread(target=self.receive_screenshot)
            receive_thread.start()
        
    
    def receive_screenshot(self):
        # Nhận độ dài dữ liệu hình ảnh
        screenshot_size_bytes = self.client.recv(4)
        screenshot_size = int.from_bytes(screenshot_size_bytes, byteorder='big')
        
        # Nhận dữ liệu hình ảnhn
        screenshot_data = b''
        remaining_data = screenshot_size
        while remaining_data > 0:
            data_chunk = self.client.recv(min(remaining_data, 4096))
            if not data_chunk:
                break
            screenshot_data += data_chunk
            remaining_data -= len(data_chunk)
            
        self.screenshot_data = screenshot_data
        self.display_screenshot(screenshot_data)

    def display_screenshot(self, screenshot_data):
        img = Image.open(io.BytesIO(screenshot_data))
        img = img.resize((400, 350), Image.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(img)
        self.picture.config(image=self.img_tk)
    
    def save_picture(self):
        if self.screenshot_data:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                with open(file_path, "wb") as f:
                    f.write(self.screenshot_data)
                    
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
    app = PicProcess(None, None)
    root.mainloop()







