import tkinter as tk
import os
import serial
import serial.tools.list_ports

def draw_grid(canvas, width, height, base_spacing=100, scale=1.0):
    """Draws a green grid on a black background, adjusting spacing dynamically and adding axis lines."""
    canvas.delete('grid')
    center_x, center_y = width // 2, height // 2

    # Adjust spacing dynamically to prevent excessive line density
    spacing = max(int(base_spacing * scale), 20)

    for x in range(center_x % spacing, width, spacing):
        canvas.create_line(x, 0, x, height, fill='green', tags='grid')

    for y in range(center_y % spacing, height, spacing):
        canvas.create_line(0, y, width, y, fill='green', tags='grid')

    # Draw thicker x and y axes
    canvas.create_line(center_x, 0, center_x, height, fill='white', width=2, tags='grid')  # Y-axis
    canvas.create_line(0, center_y, width, center_y, fill='white', width=2, tags='grid')  # X-axis

def update_points(canvas, points, scale=1.0):
    """Updates the canvas with new points, scaling them relative to zoom and centering on a Cartesian plane."""
    canvas.delete('points')

    if points:
        you_x, you_y = points[-1]  # 'You' is the last point
    else:
        return

    center_x, center_y = width // 2, height // 2
    offset_x, offset_y = center_x - you_x, center_y - you_y  # Centering offsets

    for i, (x, y) in enumerate(points):
        # Transform coordinates: move origin to 'You' and invert y-axis
        scaled_x = (x + offset_x) * scale
        scaled_y = (height - (y + offset_y) * scale)  # Invert y-axis

        if i == len(points) - 1:  # Last point is special
            canvas.create_oval(scaled_x-10, scaled_y-10, scaled_x+10, scaled_y+10, fill='red', outline='red', tags='points')
            canvas.create_text(scaled_x, scaled_y-20, text="You", fill='red', font=('Arial', 16), tags='points')
        else:
            canvas.create_oval(scaled_x-10, scaled_y-10, scaled_x+10, scaled_y+10, fill='green', outline='green', tags='points')

        canvas.create_text(scaled_x, scaled_y-25, text=f"({x}, {y})", fill='white', font=('Arial', 14), tags='points')

def on_zoom(event):
    """Handles zooming in and out on the radar view."""
    global zoom_scale
    zoom_scale *= 1.1 if event.delta > 0 else 0.9
    zoom_scale = max(0.1, min(zoom_scale, 10))  # Prevent excessive zooming
    canvas.delete("all")
    draw_grid(canvas, width, height, scale=zoom_scale)
    update_points(canvas, default_points, scale=zoom_scale)

def on_submit():
    """Handles text input submission and updates chat."""
    text = entry.get()
    if text:
        with open("savedChat.txt", "a") as file:
            file.write(text + "\n")
        entry.delete(0, tk.END)
        update_chat_log()

def update_chat_log():
    """Reads the chat log from the file and updates the text widget."""
    chat_log.config(state=tk.NORMAL)
    chat_log.delete(1.0, tk.END)
    if os.path.exists("savedChat.txt"):
        with open("savedChat.txt", "r") as file:
            chat_log.insert(tk.END, file.read())
    chat_log.config(state=tk.DISABLED)
    chat_log.yview(tk.END)

def auto_update():
    """Placeholder function for auto-update feature."""
    pass

def reset():
    """Placeholder function for reset feature."""
    pass

# Initialize main window
root = tk.Tk()
root.title("Radar Display")
root.geometry("1600x900")

width, height = 800, 800
zoom_scale = 1.0

# Create top button frame
top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X)

auto_update_button = tk.Button(top_frame, text="Auto Update", command=auto_update)
auto_update_button.pack(side=tk.LEFT)

reset_button = tk.Button(top_frame, text="Reset", command=reset)
reset_button.pack(side=tk.LEFT)

# Create main content frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create radar frame
radar_frame = tk.Frame(main_frame, width=width, height=height)
radar_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas = tk.Canvas(radar_frame, width=width, height=height, bg='black')
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind("<MouseWheel>", on_zoom)

draw_grid(canvas, width, height)

# Create chat frame
chat_frame = tk.Frame(main_frame, width=width, height=height)
chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

chat_scrollbar = tk.Scrollbar(chat_frame)
chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_log = tk.Text(chat_frame, width=80, height=40, font=('Arial', 14), state=tk.DISABLED, yscrollcommand=chat_scrollbar.set)
chat_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
chat_scrollbar.config(command=chat_log.yview)

entry = tk.Entry(chat_frame, width=60, font=('Arial', 14))
entry.pack()

submit_button = tk.Button(chat_frame, text="Send", font=('Arial', 14), command=on_submit)
submit_button.pack()

# Load chat history
update_chat_log()

# Default points
default_points = [(100, 100), (200, 200), (300, 300), (400, 400)]
default_points.append((450, 450))  # Last point is 'You'
update_points(canvas, default_points, scale=zoom_scale)

# Run Tkinter loop
root.mainloop()
