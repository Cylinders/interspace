import tkinter as tk
import os
import serial
import serial.tools.list_ports

def draw_grid(canvas, width, height, spacing=50):
    """Draws a green grid on a black background."""
    for x in range(0, width, spacing):
        canvas.create_line(x, 0, x, height, fill='green')
    for y in range(0, height, spacing):
        canvas.create_line(0, y, width, y, fill='green')

def update_points(canvas, points):
    """Updates the canvas with new points."""
    canvas.delete('points')
    for i, (x, y, hollow) in enumerate(points):
        if hollow:
            canvas.create_oval(x-5, y-5, x+5, y+5, outline='green', width=2, tags='points')
            canvas.create_text(x, y-10, text="You", fill='green', tags='points')
        else:
            canvas.create_oval(x-5, y-5, x+5, y+5, fill='green', outline='green', tags='points')

def on_submit():
    """Handles text input submission and updates chat."""
    text = entry.get()
    if text:
        with open("savedChat.txt", "a") as file:
            file.write(text + "\n")
        chat_log.insert(tk.END, "You: " + text + "\n")
        entry.delete(0, tk.END)

def toggle_view():
    """Toggles between radar and chat views."""
    global radar_view
    radar_view = not radar_view
    if radar_view:
        chat_frame.pack_forget()
        canvas.pack(fill=tk.BOTH, expand=True)
    else:
        canvas.pack_forget()
        chat_frame.pack(fill=tk.BOTH, expand=True)


def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"Port: {port.device} - {port.description}")

list_serial_ports()

x = input("What serial port are you going to be using: ")

ser = serial.Serial(x, 115200)  # Replace COMx with the correct port (Linux/Mac: /dev/ttyACM0)
while True:
    # print(ser.readline().decode().strip())
    serIn = ser.readline().decode().strip()
    match (serIn[0]): 
        case "f": 
            print("Units: Feet")
        case "m": 
            print("Units: Metres")
        case "M": 
            print("Units: Miles")
        case "y": 
            print("Units: Yards")
        case "k": 
            print("Units: Kilometres")
    print("Location: (" + serIn[1:4] + ", " + serIn[4:7] + ")")
    if not serIn[7] == "$":
        print("Message: " + serIn[7:])
    else: 
        print("$GPS request.")
    



# Initialize main window
root = tk.Tk()
root.title("Radar Display")
root.geometry("500x550")

width, height = 500, 500
radar_view = True

# Create toggle button
toggle_button = tk.Button(root, text="Toggle View", command=toggle_view)
toggle_button.pack()

# Create canvas
canvas = tk.Canvas(root, width=width, height=height, bg='black')
canvas.pack(fill=tk.BOTH, expand=True)

# Draw grid
draw_grid(canvas, width, height)

# Create chat frame
chat_frame = tk.Frame(root, width=width, height=height)
chat_log = tk.Text(chat_frame, width=60, height=30)
chat_log.pack()
entry = tk.Entry(chat_frame, width=50)
entry.pack()
submit_button = tk.Button(chat_frame, text="Send", command=on_submit)
submit_button.pack()

# Load chat history
if os.path.exists("savedChat.txt"):
    with open("savedChat.txt", "r") as file:
        chat_log.insert(tk.END, file.read())

# Default points
default_points = [(100, 100, False), (200, 200, False), (300, 300, False), (400, 400, True)]
update_points(canvas, default_points)

# Run Tkinter loop
root.mainloop()

