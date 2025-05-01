import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import os

# Points to plot
other_modules = [(100, 100), (200, 200), (300, 300)]
you = (450, 450)

# Tkinter setup
root = tk.Tk()
root.title("Radar Display with Matplotlib")
root.geometry("1600x900")
root.configure(bg='white')

# Frames
top_frame = tk.Frame(root, bg='white')
top_frame.pack(fill=tk.X)

main_frame = tk.Frame(root, bg='white')
main_frame.pack(fill=tk.BOTH, expand=True)

radar_frame = tk.Frame(main_frame, width=800, height=800, bg='white')
radar_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

chat_frame = tk.Frame(main_frame, bg='white')
chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Buttons
def auto_update():
    pass

def reset():
    pass

auto_update_button = tk.Button(top_frame, text="Auto Update", command=auto_update, bg='white')
auto_update_button.pack(side=tk.LEFT)

reset_button = tk.Button(top_frame, text="Reset", command=reset, bg='white')
reset_button.pack(side=tk.LEFT)

# Matplotlib Figure
fig, ax = plt.subplots()
fig.patch.set_facecolor("white")
ax.set_facecolor("white")
ax.set_title("Module Positions", color="black")
ax.set_xlabel("X Axis", color='black')
ax.set_ylabel("Y Axis", color='black')

# Style axes and ticks for white background
ax.tick_params(axis='x', colors='black')
ax.tick_params(axis='y', colors='black')
for spine in ax.spines.values():
    spine.set_color('black')

# Plot points
for x, y in other_modules:
    ax.scatter(x, y, color='green')
    ax.text(x + 5, y + 5, "OTHER MODULES", color='green', fontsize=9)

x, y = you
ax.scatter(x, y, color='red')
ax.text(x + 5, y + 5, "YOU", color='red', fontsize=9)

ax.grid(True, color='lightgray', linestyle='--', linewidth=0.5)

# Embed matplotlib figure in Tkinter
canvas = FigureCanvasTkAgg(fig, master=radar_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Add the navigation toolbar for zooming and panning
toolbar = NavigationToolbar2Tk(canvas, radar_frame)
toolbar.update()
toolbar.pack(side=tk.BOTTOM, fill=tk.X)

# Chat functionality
def on_submit():
    text = entry.get()
    if text:
        with open("savedChat.txt", "a") as file:
            file.write(text + "\n")
        entry.delete(0, tk.END)
        update_chat_log()

def update_chat_log():
    chat_log.config(state=tk.NORMAL)
    chat_log.delete(1.0, tk.END)
    if os.path.exists("savedChat.txt"):
        with open("savedChat.txt", "r") as file:
            chat_log.insert(tk.END, file.read())
    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

chat_scrollbar = tk.Scrollbar(chat_frame, bg='white')
chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_log = tk.Text(chat_frame, width=80, height=40, font=('Arial', 14), state=tk.DISABLED, yscrollcommand=chat_scrollbar.set, bg='white')
chat_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
chat_scrollbar.config(command=chat_log.yview)

entry = tk.Entry(chat_frame, width=60, font=('Arial', 14), bg='white')
entry.pack()

submit_button = tk.Button(chat_frame, text="Send", font=('Arial', 14), command=on_submit, bg='white')
submit_button.pack()

update_chat_log()

# Run Tkinter loop
root.mainloop()
