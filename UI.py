import csv
import serial
import tkinter as tk
from tkinter import ttk, font
# 串口設定
arduino_port = 'COM4'
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)
file_path = "Student.csv"

# 建立 UI 視窗
window = tk.Tk()
window.title("停車場資訊")
st = ttk.Style(window)
st.configure(".", font=('Helvetica', 10), padding=10)
st.configure("Title.TLabel", font=('Helvetica', 15, 'bold'))
st.configure("Clear.TButton", foreground="blue")

# 建立一個顯示"A停車場"訊息的框架和文字框
frame_a = ttk.Frame(window)
frame_a.pack(fill='both', expand="true")
label_a = ttk.Label(frame_a, text='A停車場', style="Title.TLabel")
label_a.pack(side=tk.TOP, padx=10, pady=20)
data_text_a = tk.Text(frame_a, height=10, width=50)
data_text_a.pack(side=tk.BOTTOM, padx=10, pady=10)

# 建立一個顯示"B停車場"訊息的框架和文字框
frame_b = ttk.Frame(window)
frame_b.pack(fill='both', expand="true")
label_b = ttk.Label(frame_b, text='B停車場', style="Title.TLabel")
label_b.pack(side=tk.TOP, padx=10, pady=20)
data_text_b = tk.Text(frame_b, height=10, width=50)
data_text_b.pack(side=tk.BOTTOM, padx=10, pady=10)

# 建立一個清除按鈕
clear_button = ttk.Button(window, text='Clear', style='Clear.TButton', command=lambda: clear_clicked())
clear_button.pack(side=tk.BOTTOM, padx=10, pady=10)

def clear_clicked():
     data_text_a.delete(1.0, tk.END)
     data_text_b.delete(1.0, tk.END)

# 更新 CSV 檔案中的區域信息
def update_area_in_csv(uid, area):
     # 讀取所有學生資料到列表
     students = []
     with open(file_path, mode='r') as file:
         csv_reader = csv.DictReader(file)
         for row in csv_reader:
             if row['UID'] == uid:
                 row['Area'] = area # 更新區域信息
             students.append(row)
    
     # 將更新後的資料寫回 CSV
     with open(file_path, mode='w', newline='') as file:
         fieldnames = ['ID', 'UID', 'carID', 'fine', 'MONEY', 'Area'] # 根據 CSV 檔案實際欄位進行調整
         csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
         csv_writer.writeheader()
         for student in students:
             csv_writer.writerow(student)

# 處理資料函數
def handle_data():
     # 從串口讀取數據
     if ser.in_waiting > 0:
         data = ser.readline().decode('utf-8').rstrip()
         if ',' in data:
             reader_number, uid = data.split(',') # 分割資料為讀卡機編號和UID
             match_info = f"收到UID: {uid}\n"
             area = "A" if reader_number == "1" else "B" # 假設讀卡機1是停車區A，讀卡機2是區B
             update_area_in_csv(uid, area) # 更新 CSV 中的區域資訊
            
             # 打開 CSV 檔案進行匹配
             with open(file_path, mode='r') as file:
                 csv_reader = csv.DictReader(file)
                 for row in csv_reader:
                     if row['UID'] == uid:
                         match_info += "找到符合的記錄:\n"
                         match_info += f"學號: {row['ID']}\n"
                         match_info += f"車牌號碼: {row['carID']}\n"
                         match_info += f"是否有罰單: {row['fine']}\n"
                         if row['fine'] == 'YES':
                             match_info += f"罰單金額: {row['MONEY']}\n"
                         break
                 else:
                     match_info += "未找到符合的記錄\n"
                    
             # 根據讀卡機編號選擇顯示內容的位置，在插入新的資訊之前，清空文字方塊
             if reader_number == '1':
                 data_text_a.delete('1.0', tk.END)
                 data_text_a.insert(tk.END, match_info + "\n")
             elif reader_number == '2':
                 data_text_b.delete('1.0', tk.END)
                 data_text_b.insert(tk.END, match_info + "\n")

# 定時器循環讀取串口數據
def serial_loop():
     handle_data()
     # 每隔 100 毫秒檢查串口
     window.after(100, serial_loop)

# 啟動串列埠資料讀取循環
serial_loop()

# 運行 UI 主循環
window.mainloop()