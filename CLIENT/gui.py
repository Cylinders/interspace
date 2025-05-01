import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import os
import threading
import serial.tools.list_ports
import interspace
import time
from datetime import datetime

# --------- Interspace Setup with Popup Port Selection ---------

# Connect to Interspace
api = interspace.Interspace()

# --------- Tkinter Setup ---------

root = tk.Tk()
root.title("Radar Display with Matplotlib")
root.geometry("1600x900")
root.configure(bg='white')

top_frame = tk.Frame(root, bg='white')
top_frame.pack(fill=tk.X)

main_frame = tk.Frame(root, bg='white')
main_frame.pack(fill=tk.BOTH, expand=True)

radar_frame = tk.Frame(main_frame, width=800, height=800, bg='white')
radar_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

chat_frame = tk.Frame(main_frame, bg='white')
chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# --------- Buttons ---------

def auto_update():
    pass

def reset():
    pass

auto_update_button = tk.Button(top_frame, text="Auto Update", command=auto_update, bg='white')
auto_update_button.pack(side=tk.LEFT)

reset_button = tk.Button(top_frame, text="Reset", command=reset, bg='white')
reset_button.pack(side=tk.LEFT)

# --------- Matplotlib Setup ---------

fig, ax = plt.subplots()
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
ax.set_title("Module Positions", color="black")
ax.set_xlabel("X Axis", color='black')
ax.set_ylabel("Y Axis", color='black')

ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
for spine in ax.spines.values():
    spine.set_color('black')

# Default points
other_modules = [(100, 100), (200, 200), (300, 300)]
you = (450, 450)

for x, y in other_modules:
    ax.scatter(x, y, color='green')
    ax.text(x + 5, y + 5, "OTHER MODULES", color='green', fontsize=9)

x, y = you
ax.scatter(x, y, color='red')
ax.text(x + 5, y + 5, "YOU", color='red', fontsize=9)

ax.grid(True, color='lightgray', linestyle='--', linewidth=0.5)

canvas = FigureCanvasTkAgg(fig, master=radar_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas, radar_frame)
toolbar.update()
toolbar.pack(side=tk.BOTTOM, fill=tk.X)

# --------- Chat Setup ---------

def get_timestamp():
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def on_submit():
    text = entry.get()
    target_text = target_entry.get()
    if text or target_text:
        timestamp = get_timestamp()
        message_lines = []
        line = f"{timestamp} Target: {target_text}\n"
        message_lines.append(line)
        api.sendMessage(target_text, text)

        with open("savedChat.txt", "a") as file:
            file.writelines(message_lines)
        # Append directly to chat log
        chat_log.config(state=tk.NORMAL)
        for line in message_lines:
            chat_log.insert(tk.END, line)
        chat_log.config(state=tk.DISABLED)
        chat_log.yview(tk.END)

        entry.delete(0, tk.END)
        target_entry.delete(0, tk.END)

def on_reset():
    timestamp = get_timestamp()
    line = f"{timestamp} Chat log cleared\n"

    # Clear the saved chat file, but add a reset message
    with open("savedChat.txt", "w") as file:
        file.write(line)

    # Clear and update the chat log display
    chat_log.config(state=tk.NORMAL)
    chat_log.delete(1.0, tk.END)
    chat_log.insert(tk.END, line)
    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

    # Clear entry fields
    entry.delete(0, tk.END)
    target_entry.delete(0, tk.END)

def update_chat_log():
    chat_log.config(state=tk.NORMAL)
    chat_log.delete(1.0, tk.END)
    if os.path.exists("savedChat.txt"):
        with open("savedChat.txt", "r") as file:
            chat_log.insert(tk.END, file.read())
    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

# Chat log and scrollbar
chat_log = tk.Text(chat_frame, width=80, height=40, font=('Arial', 14), state=tk.DISABLED, bg='white', wrap='word')
chat_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

chat_scrollbar = tk.Scrollbar(chat_frame, command=chat_log.yview)
chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_log.config(yscrollcommand=chat_scrollbar.set)

# Entry fields and labels
entry = tk.Entry(chat_frame, width=60, font=('Arial', 14), bg='white')
entry.pack()

target_label = tk.Label(chat_frame, text="ENTER TARGET", font=('Arial', 12), bg='white')
target_label.pack()
target_entry = tk.Entry(chat_frame, width=60, font=('Arial', 14), bg='white')
target_entry.pack()

submit_button = tk.Button(chat_frame, text="Send", font=('Arial', 14), command=on_submit, bg='white')
submit_button.pack()

clear_button = tk.Button(chat_frame, text="Clear Chat", font=('Arial', 14), command=on_reset, bg='white')
clear_button.pack()

update_chat_log()

# --------- Background Thread to Read Incoming Messages ---------

def read_from_module():
    while True:
        try:
            msg = api.readMessage()
            print("API MESSAGE: " + msg)
            if msg != -1 and msg != "":

                sender = msg[20:27]
                content = msg[27:]

                timestamp = get_timestamp()
                line = f"{timestamp} Message: {content}\n"
                with open("savedChat.txt", "a") as file:
                    file.write("Sender: " + sender)
                    file.write(line)
                # Update chat log in the main thread
                chat_log.after(0, lambda: append_to_chat_log(line))

        except Exception as e:
            print(f"Error reading from module: {e}")
        time.sleep(0.1)

def append_to_chat_log(line):
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, line)
    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

# Start background thread
print("starting read thread")
t = threading.Thread(target=read_from_module, daemon=True)
t.start()
print("starting main thread")
# --------- Start Mainloop ---------
root.mainloop()
