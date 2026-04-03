import tkinter as tk
from tkinter import messagebox
import threading
import time
import json
import os

from adb_utils import check_device, tap, swipe, launch_app, get_screen_size

running = False
click_thread = None
PRESET_FILE = "presets.json"


def load_preset():
    if os.path.exists(PRESET_FILE):
        try:
            with open(PRESET_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                preset = data.get("default", {})
                x_entry.delete(0, tk.END)
                x_entry.insert(0, str(preset.get("x", 500)))

                y_entry.delete(0, tk.END)
                y_entry.insert(0, str(preset.get("y", 1500)))

                interval_entry.delete(0, tk.END)
                interval_entry.insert(0, str(preset.get("interval", 1.0)))

                package_entry.delete(0, tk.END)
                package_entry.insert(0, preset.get("package", "com.android.settings"))
        except:
            pass


def save_preset():
    try:
        data = {
            "default": {
                "x": int(x_entry.get().strip()),
                "y": int(y_entry.get().strip()),
                "interval": float(interval_entry.get().strip()),
                "package": package_entry.get().strip()
            }
        }
        with open(PRESET_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("저장 완료", "프리셋이 저장되었습니다.")
    except Exception as e:
        messagebox.showerror("저장 오류", str(e))


def update_device_status():
    connected, device_id = check_device()
    if connected:
        status_device.config(text=f"기기 상태: 연결됨 ({device_id})", fg="green")
    else:
        status_device.config(text="기기 상태: 연결 안 됨", fg="red")
    return connected


def show_screen_size():
    if not update_device_status():
        messagebox.showwarning("연결 오류", "기기가 연결되어 있지 않습니다.")
        return
    size = get_screen_size()
    messagebox.showinfo("화면 크기", f"ADB 화면 정보:\n{size}")


def tap_once():
    if not update_device_status():
        messagebox.showwarning("연결 오류", "기기가 연결되어 있지 않습니다.")
        return

    try:
        x = int(x_entry.get().strip())
        y = int(y_entry.get().strip())
    except:
        messagebox.showwarning("입력 오류", "X, Y 좌표를 숫자로 입력하세요.")
        return

    tap(x, y)


def click_loop():
    global running
    while running:
        try:
            x = int(x_entry.get().strip())
            y = int(y_entry.get().strip())
            interval = float(interval_entry.get().strip())
            tap(x, y)
            time.sleep(interval)
        except:
            time.sleep(1)


def start_clicking():
    global running, click_thread

    if not update_device_status():
        messagebox.showwarning("연결 오류", "기기가 연결되어 있지 않습니다.")
        return

    try:
        int(x_entry.get().strip())
        int(y_entry.get().strip())
        float(interval_entry.get().strip())
    except:
        messagebox.showwarning("입력 오류", "좌표와 간격 값을 확인하세요.")
        return

    if running:
        return

    running = True
    status_run.config(text="실행 상태: 작동 중", fg="green")
    click_thread = threading.Thread(target=click_loop, daemon=True)
    click_thread.start()


def stop_clicking():
    global running
    running = False
    status_run.config(text="실행 상태: 정지", fg="red")


def swipe_test():
    if not update_device_status():
        messagebox.showwarning("연결 오류", "기기가 연결되어 있지 않습니다.")
        return
    swipe(500, 1500, 500, 500, 300)


def open_app():
    if not update_device_status():
        messagebox.showwarning("연결 오류", "기기가 연결되어 있지 않습니다.")
        return

    package = package_entry.get().strip()
    if not package:
        messagebox.showwarning("입력 오류", "패키지명을 입력하세요.")
        return

    launch_app(package)


# GUI
root = tk.Tk()
root.title("Galaxy A15 ADB Auto Clicker")
root.geometry("450x500")
root.resizable(False, False)

title = tk.Label(root, text="갤럭시 A15 ADB 자동 클릭기", font=("맑은 고딕", 14, "bold"))
title.pack(pady=10)

status_device = tk.Label(root, text="기기 상태: 확인 전", fg="blue", font=("맑은 고딕", 10, "bold"))
status_device.pack(pady=5)

check_btn = tk.Button(root, text="기기 연결 확인", command=update_device_status, width=22, height=2)
check_btn.pack(pady=5)

screen_btn = tk.Button(root, text="화면 크기 확인", command=show_screen_size, width=22, height=2)
screen_btn.pack(pady=5)

coord_frame = tk.Frame(root)
coord_frame.pack(pady=10)

tk.Label(coord_frame, text="X 좌표:", font=("맑은 고딕", 10)).grid(row=0, column=0, padx=5, pady=5)
x_entry = tk.Entry(coord_frame, width=12)
x_entry.grid(row=0, column=1, padx=5)

tk.Label(coord_frame, text="Y 좌표:", font=("맑은 고딕", 10)).grid(row=1, column=0, padx=5, pady=5)
y_entry = tk.Entry(coord_frame, width=12)
y_entry.grid(row=1, column=1, padx=5)

interval_frame = tk.Frame(root)
interval_frame.pack(pady=10)

tk.Label(interval_frame, text="반복 간격(초):", font=("맑은 고딕", 10)).pack(side=tk.LEFT)
interval_entry = tk.Entry(interval_frame, width=12)
interval_entry.pack(side=tk.LEFT, padx=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tap_btn = tk.Button(btn_frame, text="1회 터치", command=tap_once, width=12, height=2)
tap_btn.grid(row=0, column=0, padx=5, pady=5)

start_btn = tk.Button(btn_frame, text="자동 시작", command=start_clicking, width=12, height=2, bg="#dff0d8")
start_btn.grid(row=0, column=1, padx=5, pady=5)

stop_btn = tk.Button(btn_frame, text="정지", command=stop_clicking, width=12, height=2, bg="#f2dede")
stop_btn.grid(row=0, column=2, padx=5, pady=5)

swipe_btn = tk.Button(root, text="테스트 스와이프", command=swipe_test, width=22, height=2)
swipe_btn.pack(pady=8)

package_label = tk.Label(root, text="앱 패키지명 실행", font=("맑은 고딕", 10))
package_label.pack(pady=5)

package_entry = tk.Entry(root, width=35)
package_entry.pack(pady=5)

open_btn = tk.Button(root, text="앱 실행", command=open_app, width=22, height=2)
open_btn.pack(pady=8)

preset_frame = tk.Frame(root)
preset_frame.pack(pady=10)

save_btn = tk.Button(preset_frame, text="프리셋 저장", command=save_preset, width=14, height=2)
save_btn.grid(row=0, column=0, padx=8)

load_btn = tk.Button(preset_frame, text="프리셋 불러오기", command=load_preset, width=14, height=2)
load_btn.grid(row=0, column=1, padx=8)

status_run = tk.Label(root, text="실행 상태: 정지", fg="red", font=("맑은 고딕", 10, "bold"))
status_run.pack(pady=10)

load_preset()
root.mainloop()
